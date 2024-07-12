def identify_sql_type(sql_query):
    # Remove comments and trim whitespaces
    clean_query = re.sub(r'--.*$', '', sql_query, flags=re.MULTILINE).strip()
    
    # Remove block comments (/* ... */)
    clean_query = re.sub(r'/\*.*?\*/', '', clean_query, flags=re.DOTALL)
    
    # Split the query into lines and remove empty lines
    lines = [line.strip() for line in clean_query.split('\n') if line.strip()]

    # Concatenate lines into a single string
    cleaned_query = ' '.join(lines).upper()

    # Identify the SQL type by looking for keywords in the query
    if 'INSERT' in cleaned_query:
        return 'INSERT'
    elif 'UPDATE' in cleaned_query:
        return 'UPDATE'
    elif 'DELETE' in cleaned_query:
        return 'DELETE'
    elif 'TRUNCATE' in cleaned_query:
        return 'TRUNCATE'
    elif 'SELECT' in cleaned_query:
        return 'SELECT'
    else:
        return 'UNKNOWN'
