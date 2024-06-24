def identify_sql_type(sql_raw):
    sql_type = None

    # Check for INSERT pattern
    if re.search(r'^\s*INSERT\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'INSERT'
    
    # Check for SELECT pattern
    elif re.search(r'^\s*SELECT\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'SELECT'
    
    # Check for UPDATE pattern
    elif re.search(r'^\s*UPDATE\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'UPDATE'
    
    # Check for DELETE pattern
    elif re.search(r'^\s*DELETE\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'DELETE'
    
    # Check for TRUNCATE pattern
    elif re.search(r'^\s*TRUNCATE\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'TRUNCATE'
    
    # Check for MERGE pattern
    elif re.search(r'^\s*MERGE\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'MERGE'
    
    # Check for CREATE TABLE pattern
    elif re.search(r'^\s*CREATE\s+TABLE\b', sql_raw, re.IGNORECASE | re.MULTILINE):
        sql_type = 'CREATE TABLE'
    
    # Add more patterns as needed for other SQL operations
    
    return sql_type
