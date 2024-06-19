import re
import pandas as pd
from collections import defaultdict

def filter_comments(sql_raw):
    # Remove comments and skip lines between 'BEGIN' and 'END;'
    sql_raw = re.sub(r'--.*', '', sql_raw)
    sql_raw = re.sub(r'/\*.*?\*/', '', sql_raw, flags=re.DOTALL)
    sql_raw = re.sub(r'BEGIN.*?END;', '', sql_raw, flags=re.DOTALL | re.IGNORECASE)
    return sql_raw

def extract_source_tables(sql_raw):
    sql_raw = filter_comments(sql_raw)
    source_pattern = r'\bFROM\s+([^\s]+)|\bJOIN\s+([^\s]+)'
    source_tables = set()
    for match in re.findall(source_pattern, sql_raw, re.IGNORECASE):
        source_tables.update([table for table in match if table])
    return list(source_tables)

def extract_target_table(sql_raw):
    target_pattern = r'\bINSERT\s*/\*\+\s*APPEND\s*\*/\s*INTO\s+([^\s;\n]+)'
    sql_raw = filter_comments(sql_raw)
    target_match = re.search(target_pattern, sql_raw, re.IGNORECASE)
    target_table = target_match.group(1) if target_match else None
    return target_table

def extract_aliases(sql_raw):
    alias_pattern = r'(\w+)\s+AS\s+\(SELECT.*?FROM\s+(\w+)'  # Pattern to match aliases
    alias_dict = dict(re.findall(alias_pattern, sql_raw, re.IGNORECASE))
    return alias_dict

def extract_impacted_lines(sql_raw, tables, alias_dict):
    sql_raw = filter_comments(sql_raw)
    lines = sql_raw.split('\n')
    table_line_numbers = {table: None for table in tables}
    impacted_lines = {table: None for table in tables}
    for i, line in enumerate(lines):
        for table in tables:
            if table in line:
                table_line_numbers[table] = i + 1
                impacted_lines[table] = line

    # Include aliases in the impacted lines
    for alias, source in alias_dict.items():
        for table in tables:
            if alias in impacted_lines[table]:
                impacted_lines[table] = impacted_lines[table].replace(alias, f"{alias} ({source})")

    return table_line_numbers, impacted_lines

def main():
    path = "/corp/capital/saberconnect/calcs/counterparty/setup/sql_templates/"
    files = list(sandra.pathWalk(path, sandra.srcdb))
    sql_files = [file for file in files if file.endswith('.sql')]  # Filter SQL files
    results = []

    for i, sql_script_path in enumerate(sql_files):
        sql_raw = sandra.srcdb.read(sql_script_path).content.get('text')

        # Extract source tables, target table, aliases, and impacted lines
        source_tables = extract_source_tables(sql_raw)
        target_table = extract_target_table(sql_raw)
        alias_dict = extract_aliases(sql_raw)
        source_table_lines, source_impacted_lines = extract_impacted_lines(sql_raw, source_tables, alias_dict)
        target_table_lines, target_impacted_lines = extract_impacted_lines(sql_raw, [target_table] if target_table else [], alias_dict)

        # Ensure all arrays have the same length
        max_length = max(len(source_tables), len(source_table_lines), len(target_table_lines))
        source_tables += [None] * (max_length - len(source_tables))

        # Create DataFrame object
        data = {
            'Source Table': list(source_table_lines.keys()),
            'Target Table': [target_table] * max_length,
            'Line Number': list(source_table_lines.values()),
            'Impacted Line': [source_impacted_lines[table] for table in source_table_lines.keys()],
            'Path': [sql_script_path] * max_length  # Add path column
        }
        df = pd.DataFrame(data)

        # Append DataFrame to results list
        results.append(df)

    # Concatenate all DataFrames in the results list
    final_df = pd.concat(results, ignore_index=True)

    # Print final DataFrame
    print(final_df)

# Call the main function
main()

