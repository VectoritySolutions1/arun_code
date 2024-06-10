import re
from sqlparse import parse, tokens, sql
import sandra

def extract_tables(sql_script):
    source_tables = []
    target_tables = []

    parsed = parse(sql_script)

    for statement in parsed:
        if statement.get_type() == 'INSERT':
            target_tables += extract_insert_target(statement)
            source_tables += extract_insert_source(statement)
        elif statement.get_type() == 'SELECT':
            source_tables += extract_select_source(statement)
        elif statement.get_type() == 'UPDATE':
            target_tables += extract_update_target(statement)
            source_tables += extract_update_source(statement)
        elif statement.get_type() == 'DELETE':
            target_tables += extract_delete_target(statement)

    return {
        'source_tables': list(set(source_tables)),
        'target_tables': list(set(target_tables))
    }

def extract_insert_target(statement):
    tables = []
    for token in statement.tokens:
        if token.ttype == tokens.Keyword and token.value.upper() == 'INTO':
            table_token = statement.token_next(statement.token_index(token))
            if isinstance(table_token, sql.Identifier):
                tables.append(table_token.get_real_name())
    return tables

def extract_insert_source(statement):
    tables = []
    for token in statement.tokens:
        if isinstance(token, sql.Parenthesis):
            for sub_token in token.tokens:
                if isinstance(sub_token, sql.Identifier):
                    tables.append(sub_token.get_real_name())
    return tables

def extract_select_source(statement):
    tables = []
    for token in statement.tokens:
        if isinstance(token, sql.IdentifierList):
            for identifier in token.get_identifiers():
                tables.append(identifier.get_real_name())
        elif isinstance(token, sql.Identifier):
            tables.append(token.get_real_name())
    return tables

def extract_update_target(statement):
    tables = []
    for token in statement.tokens:
        if isinstance(token, sql.Identifier):
            tables.append(token.get_real_name())
    return tables

def extract_update_source(statement):
    tables = []
    for token in statement.tokens:
        if isinstance(token, sql.Where):
            for sub_token in token.tokens:
                if isinstance(sub_token, sql.Identifier):
                    tables.append(sub_token.get_real_name())
    return tables

def extract_delete_target(statement):
    tables = []
    for token in statement.tokens:
        if token.ttype == tokens.Keyword and token.value.upper() == 'FROM':
            table_token = statement.token_next(statement.token_index(token))
            if isinstance(table_token, sql.Identifier):
                tables.append(table_token.get_real_name())
    return tables

def main():
    path = "/corp/capital/saberconnect/calcs/counterparty/setup/sql_templates/"
    files = list(sandra.pathWalk(path, sandra.srcdb))
    results = []

    for i, sql_script_path in enumerate(files):
        sql_raw = sandra.srcdb.read(sql_script_path).content.get('text')
        tables = extract_tables(sql_raw)

        for source_table in tables['source_tables']:
            results.append({
                's_no': i + 1,
                'script_path': sql_script_path,
                'source_table': source_table,
                'target_table': tables['target_tables'][0] if tables['target_tables'] else None
            })

    # Print results in tabular format
    print(f"{'S.No.':<5} {'Script Path':<60} {'Source Table':<40} {'Target Table':<40}")
    for result in results:
        print(f"{result['s_no']:<5} {result['script_path']:<60} {result['source_table']:<40} {result['target_table']:<40}")

if __name__ == "__main__":
    main()
