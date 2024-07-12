def skip_begin_end_blocks(sql_query):
    lines = sql_query.split('\n')
    result_lines = []
    skip_block = False
    begin_found = False

    for line in lines:
        # Skip whole line comments
        if re.match(r'^\s*--', line):
            continue
        
        # Remove inline comments
        line = re.sub(r'--.*$', '', line)

        # Skip BEGIN...END blocks
        if re.search(r'\bBEGIN\b', line, re.IGNORECASE):
            skip_block = True
            begin_found = True
        elif re.search(r'\bEND\b', line, re.IGNORECASE) and begin_found:
            skip_block = False
            begin_found = False
        elif not skip_block:
            result_lines.append(line)

    return '\n'.join(result_lines)
