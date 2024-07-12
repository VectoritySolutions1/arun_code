
def find_alias_sources(sql_query):
    alias_pattern = re.compile(r'(\w+)\s+AS\s+\(\s*SELECT', re.IGNORECASE)
    from_pattern = re.compile(r'\bFROM\s+([\w.]+)', re.IGNORECASE)
    join_pattern = re.compile(r'(?:JOIN|INNER JOIN|CROSS JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([\w.]+)', re.IGNORECASE)
    
    alias_sources = []
    alias_stack = []
    alias_map = {}
    in_alias = False
    current_alias = None
    sql_lines = sql_query.split('\n')

    for line in sql_lines:
        alias_match = alias_pattern.search(line)
        if alias_match:
            alias_name = alias_match.group(1)
            alias_stack.append(alias_name)
            alias_map[alias_name] = []
            in_alias = True
            current_alias = alias_name

        if in_alias:
            from_matches = from_pattern.findall(line)
            join_matches = join_pattern.findall(line)
            if from_matches or join_matches:
                alias_map[current_alias].extend(from_matches + join_matches)
        
        open_parens = line.count('(')
        close_parens = line.count(')')
        
        if in_alias and open_parens == close_parens:
            in_alias = False
            current_alias = None
        elif in_alias and close_parens > open_parens:
            alias_stack.pop()
            if alias_stack:
                current_alias = alias_stack[-1]
            else:
                in_alias = False
                current_alias = None

    for alias, sources in alias_map.items():
        for source in sources:
            alias_sources.append((alias, source))

    df = pd.DataFrame(alias_sources, columns=['aliasname', 'sourcetable']).drop_duplicates()

    return df



def identify_tables(sql_query):
    # Regular expressions to match target and source tables
    target_pattern = re.compile(r'INSERT\s+\/\*\s*\+\s*APPEND\s*\*\/\s*INTO\s+[\w.]+\.([\w_]+)', re.IGNORECASE)
    source_pattern = re.compile(r'(?:FROM|JOIN)\s+(?:\w+\.)*(\w+)', re.IGNORECASE)  # Updated pattern

    target_match = target_pattern.search(sql_query)
    
    target_table = target_match.group(1) if target_match else None
    
    impacted_lines = []
    lines = sql_query.split('\n')

    for idx, line in enumerate(lines):
        if target_match and target_table in line:
            impacted_lines.append((target_table, None, idx + 1, line.strip()))
        for match in source_pattern.finditer(line):
            source_table = match.group(1)
            impacted_lines.append((target_table, source_table, idx + 1, line.strip()))  # Added target_table here

    # Create DataFrame
    df = pd.DataFrame(impacted_lines, columns=['targettable', 'sourcetable', 'lineno', 'impactedcontent'])

    # Replace None with empty string for better readability
    df.fillna('', inplace=True)

    return df




ef skip_begin_end_blocks(sql_query):

  lines = sql_query.split('\n')
  result_lines = []
  skip_block = False

  for line in lines:
    if re.search(r'\bBEGIN\b', line, re.IGNORECASE):
      skip_block = True
    elif re.search(r'\bEND\b', line, re.IGNORECASE):
      skip_block = False
    elif not skip_block:
      result_lines.append(line)

  return '\n'.join(result_lines)
