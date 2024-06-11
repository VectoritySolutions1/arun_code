import re
import pandas as pd

def main():
    path = "/corp/capital/saberconnect/calcs/counterparty/setup/sql_templates/"
    files = list(sandra.pathWalk(path, sandra.srcdb))
    results = []

    for i, sql_script_path in enumerate(files):
        sql_raw = sandra.srcdb.read(sql_script_path).content.get('text')

        # Extract source tables, target table, and impacted lines
        source_tables = extract_source_tables(sql_raw)
        target_table = extract_target_table(sql_raw)
        source_table_lines, source_impacted_lines = extract_impacted_lines(sql_raw, source_tables)
        target_table_lines, target_impacted_lines = extract_impacted_lines(sql_raw, [target_table] if target_table else [])

        # Ensure all arrays have the same length
        max_length = max(len(source_tables), len(source_table_lines), len(target_table_lines))
        source_tables += [None] * (max_length - len(source_tables))
        source_table_lines = {k: v for k, v in source_table_lines.items()}
        source_table_lines.update((x, 'line in used') for x in source_tables if x not in source_table_lines)

        # Create DataFrame object
        data = {
            'Source Table': list(source_table_lines.keys()),
            'Target Table': [target_table] * max_length,
            'Line Number': list(source_table_lines.values()),
            'Impacted Line': list(source_impacted_lines.values())
        }
        df = pd.DataFrame(data)

        # Append DataFrame to results list
        results.append(df)

    # Concatenate all DataFrames in the results list
    final_df = pd.concat(results, ignore_index=True)

    # Print DataFrame
    print(final_df)

def extract_source_tables(sql_raw):
    source_pattern = r'\b(?:FROM|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|OUTER JOIN|CROSS JOIN)\s+([^\s;\n]+)'
    source_matches = re.findall(source_pattern, sql_raw, re.IGNORECASE)
    unique_source_tables = list(set(source_matches))
    return unique_source_tables

def extract_target_table(sql_raw):
    target_pattern = r'\b(?:INTO)\s+([^\s;\n]+)'
    target_match = re.search(target_pattern, sql_raw, re.IGNORECASE)
    target_table = target_match.group(1) if target_match else None
    return target_table

def extract_impacted_lines(sql_raw, tables):
    lines = sql_raw.split('\n')
    table_line_numbers = {table: None for table in tables}
    impacted_lines = {table: None for table in tables}
    for i, line in enumerate(lines):
        for table in tables:
            if table in line:
                table_line_numbers[table] = i + 1
                impacted_lines[table] = line
    return table_line_numbers, impacted_lines

if __name__ == "__main__":
    main()
ou8select ***
