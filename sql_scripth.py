def skip_specific_begin_end_blocks(sql_query):
    lines = sql_query.split('\n')
    result_lines = []
    skip_block = False
    begin_found = False

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip whole line comments
        if re.match(r'^\s*--', line):
            i += 1
            continue
        
        # Remove inline comments
        line = re.sub(r'--.*$', '', line)
        
        # Check for lowercase 'begin'
        if re.match(r'^\s*begin\s*$', line):
            # Check if the next line is uppercase 'BEGIN'
            if i + 1 < len(lines) and lines[i + 1].strip().upper() == 'BEGIN':
                skip_block = True
                begin_found = True
                i += 2  # Skip 'begin' and 'BEGIN'
                continue

        if skip_block and re.match(r'^\s*END\s*$', line):
            # Check if the next line is lowercase 'end'
            if i + 1 < len(lines) and lines[i + 1].strip().lower() == 'end':
                skip_block = False
                begin_found = False
                i += 2  # Skip 'END' and 'end'
                continue

        if not skip_block:
            result_lines.append(line)
        
        i += 1

    return '\n'.join(result_lines)
