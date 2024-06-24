def identify_sql_type(sql_raw):
    sql_type = None

    # Check for INSERT /*+ APPEND */ pattern
    if re.search(r'\bINSERT\s*/\*\+\s*APPEND\s*\*/\b', sql_raw, re.IGNORECASE):
        sql_type = 'INSERT /*+ APPEND */'
    
    # Check for SELECT pattern
    elif re.search(r'\bSELECT\b', sql_raw, re.IGNORECASE):
        sql_type = 'SELECT'
    
    # Check for UPDATE pattern
    elif re.search(r'\bUPDATE\b', sql_raw, re.IGNORECASE):
        sql_type = 'UPDATE'
    
    # Check for DELETE pattern
    elif re.search(r'\bDELETE\b', sql_raw, re.IGNORECASE):
        sql_type = 'DELETE'
    
    # Check for TRUNCATE pattern
    elif re.search(r'\bTRUNCATE\b', sql_raw, re.IGNORECASE):
        sql_type = 'TRUNCATE'
    
    # Check for MERGE pattern
    elif re.search(r'\bMERGE\b', sql_raw, re.IGNORECASE):
        sql_type = 'MERGE'
    
    # Check for CREATE TABLE pattern
    elif re.search(r'\bCREATE\s+TABLE\b', sql_raw, re.IGNORECASE):
        sql_type = 'CREATE TABLE'
    
    # Add more patterns as needed for other SQL operations
    
    return sql_type
