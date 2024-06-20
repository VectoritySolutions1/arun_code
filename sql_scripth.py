import re
import pandas as pd

def filter_comments(sql_raw):
    lines = sql_raw.split('\n')
    filtered_lines = [line for line in lines if not line.strip().startswith('--')]
    return '\n'.join(filtered_lines)

def extract_alias_to_table_mapping(sql_raw):
    alias_pattern = r'(\w+)\s+AS\s+\(\s*SELECT\s+.*?\s+FROM\s+([^\s;\n\(\)]+).*?\)'
    alias_matches = re.findall(alias_pattern, sql_raw, re.IGNORECASE | re.DOTALL)
    alias_to_table = {alias: table for alias, table in alias_matches}
    return alias_to_table

def replace_aliases_with_tables(impacted_lines, alias_to_table):
    replaced_lines = {}
    for alias, table in alias_to_table.items():
        for original_line in impacted_lines:
            replaced_line = impacted_lines[original_line].replace(alias, f"{alias} ({table})")
            replaced_lines[original_line] = replaced_line
    return replaced_lines

def extract_source_tables(sql_raw):
    source_pattern = r'\b(?:FROM|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|OUTER JOIN|CROSS JOIN)\s+([^\s;\n\(\)]+)'
    nested_select_pattern = r'\b(?:FROM|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|OUTER JOIN|CROSS JOIN)\s+\(\s*SELECT\s+.*?\s+FROM\s+([^\s;\n\(\)]+).*?\)'

    sql_raw = filter_comments(sql_raw)
    source_matches = re.findall(source_pattern, sql_raw, re.IGNORECASE)
    nested_matches = re.findall(nested_select_pattern, sql_raw, re.IGNORECASE)

    all_matches = list(set(source_matches + nested_matches))
    
    # Remove 'WITH' and 'AND' patterns from source tables
    all_matches = [match for match in all_matches if not match.strip().startswith('WITH') and ' AND ' not in match]

    return all_matches

def extract_target_table(sql_raw):
    target_pattern = r'\bINSERT\s*/\*\+\s*APPEND\s*\*/\s*INTO\s+([^\s;\n]+)'
    sql_raw = filter_comments(sql_raw)
    target_match = re.search(target_pattern, sql_raw, re.IGNORECASE)
    target_table = target_match.group(1) if target_match else None
    return target_table

def extract_impacted_lines(sql_raw, tables):
    sql_raw = filter_comments(sql_raw)
    lines = sql_raw.split('\n')
    table_line_numbers = {table: None for table in tables}
    impacted_lines = {table: None for table in tables}
    for i, line in enumerate(lines):
        for table in tables:
            if table in line:
                table_line_numbers[table] = i + 1
                impacted_lines[table] = line
    return table_line_numbers, impacted_lines

def extract_key_value_pairs_A(sql_query):
    pattern = r'(\w+)\s+AS\s+\(([^()]*((?:\([^()]*\))*[^()]*)*)\)'
    matches = re.finditer(pattern, sql_query, re.DOTALL | re.IGNORECASE)

    key_value_pairs = {}

    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()

        # Extract the SQL segment
        key_value_pairs[key] = f"AS ({value})"

    return key_value_pairs

def extract_source_tables_A(sql_dict):
    source_tables_dict = {}
    
    # Regular expression pattern to find table names after FROM or JOIN
    table_pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+(?:\s*,\s*[a-zA-Z0-9_]+)*)'

    for key, sql_query in sql_dict.items():
        # Match all occurrences of table names after FROM, JOIN, etc.
        matches = re.findall(table_pattern, sql_query, re.IGNORECASE)
        
        # Store unique table names in a set
        table_names = set()
        for match in matches:
            table_names.update([t.strip() for t in match.split(',')])

        # Replace table names with corresponding keys if they exist in the dictionary
        for table_name in table_names.copy():  # Create a copy to iterate over
            if table_name in source_tables_dict:
                table_names.remove(table_name)  # Remove the original table name
                table_names.update(source_tables_dict[table_name])  # Add its corresponding values
        
        # Remove the key itself if present in table_names
        if key in table_names:
            table_names.remove(key)
        
        # Merge with existing table names or initialize if not present
        if key in source_tables_dict:
            source_tables_dict[key].update(table_names)
        else:
            source_tables_dict[key] = table_names
        
    return source_tables_dict

def update_source_table_values(data, sql_dict):
    updated_data = data.copy()  # Make a copy to avoid modifying the original data
    
    for i, source_table in enumerate(updated_data['Source Table']):
        if source_table in sql_dict:
            updated_data['Source Table'][i] = sql_dict[source_table]
    
    return updated_data


def main():
    sql_raw = """
    BEGIN
    INSERT /*+ APPEND */ INTO ECM_SABER2.CALC_INPUT_TP_DERIVATIVES_INTERMEDIATE
    SELECT * FROM
    WITH
    DATASET AS (SELECT RSLT.RESULT_DATASET_ID AS RDI, 'workstream' AS TP_WKSTRM_NM, RSLT.MAST_INPUT_DATASET_ID AS MIDI, MAST.INPUT_DATASET_ID AS IDI, RSLT.ORIG_MAST_INPUT_DATASET_ID AS IDI
    FROM S_SYS_LOAD_RESULT_DATASET RSLT JOIN S_SYS_LOAD_INPUT_DATASET MAST MAST
    ON RSLT.MAST_INPUT_DATASET_ID = MAST.MAST_INPUT_DATASET_ID AND RSLT.ACTIVE_FLAG = 'N' AND RSLT.STATUS_CD = 0 AND MAST.GROUP_NM = '{group_name}' AND RSLT.WORKSTREAM
    AND RSLT.PER_KEY = {PerKey}),
    VRI_CPT AS (SELECT V.*, (SELECT MIDI FROM DATASET) AS MIDI FROM VRI_TRAD_PROD_CNTPY V WHERE PER_KEY = {PerKey} AND INPUT_DATASET_ID = (SELECT IDI FROM DATASET)),
    VRT_DERIV AS (SELECT V.*, (SELECT MIDI FROM DATASET) AS MIDI FROM VRI_TRAD_PROD_DERIVATIVES V WHERE PER_KEY = {PerKey} AND INPUT_DATASET_ID = (SELECT IDI FROM DATASET)),
    CCPT AS (SELECT C.*, (SELECT IDI FROM DATASET) AS INPUT_DATASET_ID, (SELECT OMIDI FROM DATASET) AS OMIDI FROM VRI_TRAD_PROD_CNTPY C WHERE PER_KEY = {PerKey}),
    IMM_TRADE AS (SELECT PER_KEY, C.CAP_EXPOSURE_ID, C.CEM_CD, C.UNUSED_CTRL_PCT, C.CS_NETTING_SET_ID, C.MAST_INPUT_DATASET_ID, JURISDICTION_CD = 'US' AND PER_KEY = {PerKey} AND MAST_INPUT_DATASET_ID = (SELECT MIDI FROM DATASET)),
    SELECT
    {PerKey} AS PER_KEY
    , IDER.CAP_EXPOSURE_ID
    , IDER.AS_OF_DT AS AS_OF_DT
    , IDER.ARCTIC_SYS_GEN_ID AS ARCTIC_SYS_GEN_ID
    , IDER.BASEL_PRODUCT_GROUP AS BASEL_PRODUCT_GROUP
    , IDER.BASEL_PRODUCT_TYPE AS BASEL_PRODUCT_TYPE
    , CASE WHEN IDER.QUALIFYING_REFERENCE_ASSET_FLAG = 'Y' THEN 1
    ELSE 0 END AS QUALIFYING_REFERENCE_ASSET_FLAG
    , CASE WHEN IDER.QUALIFYING_REFERENCE_ASSET_FLAG = 'N' THEN 0 END AS QUALIFYING_REFERENCE_ASSET_FLAG
    , IDER.GCI_NBR AS GCI_NBR
    , IDER.TRADE_ID AS TRADE_ID
    , TO_CHAR(IDER.TRADE_DT,'YYYY-MM-DD') AS TRADE_DT
    , TO_CHAR(IDER.MATURITY_DT,'YYYY-MM-DD') AS MATURITY_DT
    , TO_CHAR(IDER.SETTLEMENT_DT,'YYYY-MM-DD') AS SETTLEMENT_DT
    FROM IDER
    WHEN UPPER(TRIM(IDER.NETTING_ALLOWED_FLAG)) = 'N' THEN 0
    ELSE NULL
    END AS NETTING_ALLOWED_FLAG
    , IDER.BOOKMAP_ID AS BOOKMAP_TB_ID
    , IDER.TRADING_BOOK_ID AS BOOKMAP_TB_NM
    , IDER.CNR_ATTRIBUTE AS CNR_ATTRIBUTE
    , IDER.GL_ACCOUNT_NBR AS GL_ACCOUNT_NBR
    , IDER.COMPANY AS COMPANY_ORIG
    , IDER.COST_CENTER AS COST_CENTER_ORIG
    , IDER.FEED_NAME AS FEED_NAME
    , COALESCE(IDER.TRADE_TYPE, 'NA') AS TRADE_TYPE
    , IDER.INSTRUMENT_CD AS INSTRUMENT_CD
    , IDER.SOURCE_PRODUCT_CD AS SOURCE_PRODUCT_CD
    , IDER.TRANSACTION_ID AS TRANSACTION_ID
    , IDER.DEAL_ID AS DEAL_ID
    , IDER.SYSTEM_OF_RECORD AS SYSTEM_OF_RECORD
    , IDER.CTRL_FLAG AS CTRL_FLAG
    , IMM_TRADE.CEM_CD AS CEM_CD
    , IMM_TRADE.CEM_CD_RISK AS CEM_CD_RISK
    , IDER.DIRECTION_CD AS DIRECTION_CD
    , IDER.MARGIN_TYPE AS MARGIN_TYPE
    , VRI_DERIV.BUY_SELL_CD_ORIG AS BUY_SELL_CD_ORIG
    , IDER.BUY_SELL_CD AS BUY_SELL_CD
    , IDER.GCI_NBR AS GCI_NBR
    , IDER.CDS_REFERENCE_ENTITY_GCI_NBR AS REFERENCE_ENTITY_GCI_NBR
    , IDER.CDS_REFERENCE_ENTITY_COPER_ID AS REFERENCE_ENTITY_COPER_ID
    , IDER.CDS_NETTING_SET_ID AS CDS_NETTING_SET_ID
    , IDER.REFERENCE_ASSET_TRADE_LINK AS REFERENCE_ASSET_TRADE_LINK
    , IDER.RWA_TREATMENT_OVERRIDE_CD AS RWA_TREATMENT_OVERRIDE_CD
    , TO_CHAR(IDER.TRADE_DT,'YYYY-MM-DD') AS TRADE_DT
    , TO_CHAR(IDER.MATURITY_DT,'YYYY-MM-DD') AS MATURITY_DT
    , TO_CHAR(IDER.SETTLEMENT_DT,'YYYY-MM-DD') AS SETTLEMENT_DT
    , IDER.ACTUAL_SETTLEMENT_DT AS ACTUAL_SETTLEMENT_DT
    BEGIN SABERTWO 56488/56390 IMELDA
    , IDER.LOWER BARRIER LVL
    , IDER.UPPER BARRIER LVL
    , IDER.CAP
    , IDER.FLOOR VALUE
    END SABERTWO 56488/56390 IMELDA
    , IDER.NOTIONAL USD AMT ARCTIC = SABERTWO 56657/56696 IMELDA
    FROM CDERIV IDER
    LEFT JOIN VRI_DERIV
    ON IDER.PER_KEY = VRI_DERIV.PER_KEY AND IDER.MAST_INPUT_DATASET_ID = VRI_DERIV.MIDI
    AND IDER.INPUT_DATASET_ID = VRI_DERIV.INPUT_DATASET_ID AND IDER.OMIDI = VRI_DERIV.MAST_INPUT_DATASET_ID
    AND TRIM(IDER.DERIVED_SYS_GEN_ID) = TRIM(VRI_DERIV
    LEFT JOIN VRI_CPT
    ON IDER.PER_KEY = VRI_CPT.PER_KEY AND IDER.MAST_INPUT_DATASET_ID = V
    CPT.MIDI
    AND IDER.INPUT_DATASET_ID = VRI_CPT.INPUT_DATASET_ID AND IDER.OMIDI = VRI_CPT.MAST_INPUT_DATASET_ID
    AND IDER.GCI_NBR = VRI_CPT.GCI_NBR
    LEFT JOIN VRI_CPT VRTCNTPY
    ON IDER.PER_KEY = VRTCNTPY.PER_KEY AND IDER.MAST_INPUT_DATASET_ID = VRTCNTPY.MAST_INPUT_DATASET_ID
    AND IDER.INPUT_DATA
    """

    alias_to_table = extract_alias_to_table_mapping(sql_raw)

    # Extract source tables, target table, and impacted lines
    source_tables = extract_source_tables(sql_raw)
    target_table = extract_target_table(sql_raw)
    source_table_lines, source_impacted_lines = extract_impacted_lines(sql_raw, source_tables)
    target_table_lines, target_impacted_lines = extract_impacted_lines(sql_raw, [target_table] if target_table else [])

    # Replace aliases with their corresponding source tables
    replaced_source_impacted_lines = replace_aliases_with_tables(source_impacted_lines, alias_to_table)

    # Ensure all arrays have the same length
    max_length = max(len(source_tables), len(source_table_lines), len(target_table_lines))
    source_tables += [None] * (max_length - len(source_tables))

    # Create DataFrame object
    data = {
        'Source Table': list(source_table_lines.keys()),
        'Target Table': [target_table] * max_length,
        'Line Number': list(source_table_lines.values()),
        'Impacted Line': [replaced_source_impacted_lines[table] for table in source_table_lines.keys()],
    }

    # Extract key-value pairs from the SQL query
    key_value_pairs = extract_key_value_pairs_A(sql_raw)

    print(key_value_pairs)

    # Extract source tables for each CTE
    source_tables_dict = extract_source_tables_A(key_value_pairs)
    data = update_source_table_values(data, source_tables_dict )



    df = pd.DataFrame(data)

    # Print final DataFrame
    print(df)

# Call the main function
if __name__ == "__main__":
    main()

