import re
import pandas as pd

def filter_comments(sql_raw):
    lines = sql_raw.split('\n')
    filtered_lines = [line for line in lines if not line.strip().startswith('--')]
    return '\n'.join(filtered_lines)

def extract_alias_to_table_mapping(sql_raw):
    alias_pattern = r'(\w+)\s+AS\s*\(\s*SELECT\s+.*?\s+FROM\s+([^\s;\n\(\)]+).*?\)'
    alias_matches = re.findall(alias_pattern, sql_raw, re.IGNORECASE | re.DOTALL)
    alias_to_table = {alias: table for alias, table in alias_matches}
    return alias_to_table

def replace_aliases(sql_raw, alias_to_table):
    for alias, table in alias_to_table.items():
        sql_raw = re.sub(r'\b' + re.escape(alias) + r'\b', table, sql_raw)
    return sql_raw

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


def extract_alias_source_mappings(sql_script):
    """
    Extracts alias names and their corresponding SQL statements from the SQL script.

    Args:
    - sql_script (str): SQL script where alias names and source tables need to be extracted.

    Returns:
    - dict: Dictionary containing alias as keys and corresponding SQL statements as values.
    """
    alias_source_mappings = {}

    # Pattern to capture alias and SQL statement until the closing parenthesis
    alias_pattern = r"\b([A-Za-z0-9_]+)\s+AS\s*\("

    # Find all matches for aliases
    alias_matches = re.finditer(alias_pattern, sql_script, re.IGNORECASE | re.DOTALL)

    for match in alias_matches:
        alias = match.group(1)
        start = match.end() - 1  # Start at the opening parenthesis
        end = find_closing_parenthesis(sql_script, start)
        sql_statement = sql_script[start:end].strip()
        alias_source_mappings[alias] = sql_statement

    return alias_source_mappings

def find_closing_parenthesis(sql_script, start_pos):
    """
    Finds the position of the closing parenthesis matching the first opening parenthesis.

    Args:
    - sql_script (str): SQL script containing the text.
    - start_pos (int): Position of the first opening parenthesis.

    Returns:
    - int: Position of the matching closing parenthesis.
    """
    open_parens = 0
    for pos in range(start_pos, len(sql_script)):
        if sql_script[pos] == '(':
            open_parens += 1
        elif sql_script[pos] == ')':
            open_parens -= 1
            if open_parens == 0:
                return pos + 1  # Return position after the closing parenthesis

    raise ValueError("No matching closing parenthesis found")

def extract_source_tables_A(sql_statement):

    source_tables = []

    # Pattern to find table names after keywords like FROM, JOIN, etc.
    pattern = r'\b(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN|CROSS JOIN)\s+([A-Za-z0-9_]+)'
    matches = re.findall(pattern, sql_statement, re.IGNORECASE)

    # Add matched tables to the list of source tables
    source_tables.extend(matches)

    return source_tables

def replace_aliases(sql_statement, alias_source_mappings):
    """
    Replaces alias names in the SQL statement with their corresponding SQL statements from the dictionary.

    Args:
    - sql_statement (str): SQL statement where alias names need to be replaced.
    - alias_source_mappings (dict): Dictionary containing alias as keys and corresponding SQL statements as values.

    Returns:
    - str: SQL statement with aliases replaced.
    """
    for alias, replacement in alias_source_mappings.items():
        sql_statement = re.sub(r'\b' + re.escape(alias) + r'\b', replacement, sql_statement)
    return sql_statement

import pandas as pd

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
AND TRIM(IDER.DERIVED_SYS_GEN_ID) = TRIM(VRI_DERIV.SRC_CAP_EXPOSURE_ID)
AND TRIM(IDER.BASEL_PRODUCT_TYPE) = TRIM(VRI_DERIV.BASEL_PRODUCT_TYPE)
LEFT JOIN VRI_CPT
ON IDER.PER_KEY = VRI_CPT.PER_KEY AND IDER.MAST_INPUT_DATASET_ID = VRI_CPT.MIDI
AND IDER.INPUT_DATASET_ID = VRI_CPT.INPUT_DATASET_ID AND IDER.OMIDI = VRI_CPT.MAST_INPUT_DATASET_ID
AND IDER.GCI_NBR = VRI_CPT.GCI_NBR
LEFT JOIN VRI_CPT VRTCNTPY
ON IDER.PER_KEY = VRTCNTPY.PER_KEY AND IDER.MAST_INPUT_DATASET_ID = VRTCNTPY.MAST_INPUT_DATASET_ID
AND IDER.INPUT_DATA
    """

    # Step 1: Filter comments
    sql_raw = filter_comments(sql_raw)

    alias_source_mappings = extract_alias_source_mappings(sql_raw)
    print("Alias Source Mappings:")
    print(alias_source_mappings)

    # Replace aliases with their corresponding SQL statements and extract source tables
    source_tables = {}
    for alias, sql_statement in alias_source_mappings.items():
        replaced_statement = replace_aliases(sql_statement, alias_source_mappings)
        tables = extract_source_tables_A(replaced_statement)
        source_tables[alias] = list(set(tables))  # Remove duplicates

    print("Source Tables:")
    for k,v in source_tables.items():
        print(f"{k} -------> {v}")

    # Step 2: Extract alias-to-table mappings
    alias_to_table = extract_alias_to_table_mapping(sql_raw)

    # Step 3: Replace aliases with their corresponding source tables
    sql_raw_replaced = replace_aliases(sql_raw, alias_to_table)

    # Step 4: Extract source tables
    source_tables_main = extract_source_tables(sql_raw_replaced)

    # Step 5: Extract target table
    target_table = extract_target_table(sql_raw)

    # Step 6: Extract impacted lines
    source_table_lines, source_impacted_lines = extract_impacted_lines(sql_raw_replaced, source_tables_main)
    target_table_lines, target_impacted_lines = extract_impacted_lines(sql_raw, [target_table] if target_table else [])

    # Ensure all arrays have the same length
    max_length = max(len(source_tables_main), len(source_table_lines), len(target_table_lines))
    source_tables_main += [None] * (max_length - len(source_tables_main))

    # Step 7: Prepare the data dictionary
    data = {
        'Source Table': list(source_table_lines.keys()),
        'Target Table': [target_table] * max_length,
        'Line Number': list(source_table_lines.values()),
        'Impacted Line': [source_impacted_lines[table] for table in source_table_lines.keys()],
    }
        # Extend source table values with alias mappings

    df_1 = pd.DataFrame(data)
    print(df_1)
    print(data['Source Table'])
    for key, value in source_tables.items():
            print("--------->",key)
            
            if key in data['Source Table']:
                index = data['Source Table'].index(key)
                data['Source Table'][index] = value

    # Ensure all arrays have the same length again after extension
    max_length = max(len(data['Source Table']), len(data['Line Number']), len(data['Impacted Line']))

    data['Source Table'] += [None] * (max_length - len(data['Source Table']))

    # Create DataFrame object
    df = pd.DataFrame(data)

    # Print final DataFrame
    print("\nFinal DataFrame:")
    print(df)

# Call the main function
main()




