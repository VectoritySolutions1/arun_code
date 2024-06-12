import re
import pandas as pd

def extract_source_tables(sql_raw):
    # Pattern to match tables in FROM and JOIN clauses
    source_pattern = r'\b(?:FROM|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|OUTER JOIN|CROSS JOIN)\s+([^\s;\n\(\)]+)'
    
    # Pattern to match nested SELECT statements and extract tables within them
    nested_select_pattern = r'\b(?:FROM|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|OUTER JOIN|CROSS JOIN)\s+\(\s*SELECT\s+.*?\s+FROM\s+([^\s;\n\(\)]+).*?\)'
    
    source_matches = re.findall(source_pattern, sql_raw, re.IGNORECASE)
    nested_matches = re.findall(nested_select_pattern, sql_raw, re.IGNORECASE)
    
    # Combine and deduplicate source tables
    all_matches = list(set(source_matches + nested_matches))
    return all_matches

def extract_target_table(sql_raw):
    target_pattern = r'\bINSERT\s*/\*\+\s*APPEND\s*\*/\s*INTO\s+([^\s;\n]+)'
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



source_tables = extract_source_tables(sql_raw)
target_table = extract_target_table(sql_raw)

source_table_lines, source_impacted_lines = extract_impacted_lines(sql_raw, source_tables)
target_table_lines, target_impacted_lines = extract_impacted_lines(sql_raw, [target_table] if target_table else [])

# Ensure all arrays have the same length
max_length = max(len(source_tables), len(source_table_lines), len(target_table_lines))
source_tables += [None] * (max_length - len(source_tables))

# Create DataFrame object
data = {
    'Source Table': list(source_table_lines.keys()),
    'Target Table': [target_table] * max_length,
    'Line Number': list(source_table_lines.values()),
    'Impacted Line': [source_impacted_lines[table] for table in source_table_lines.keys()]
}
df = pd.DataFrame(data)

# Print DataFrame
print(df)
