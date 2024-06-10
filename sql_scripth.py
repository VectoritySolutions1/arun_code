import re
from sqlparse import parse, tokens, sql
import sandra

def extract_tables_with_line_numbers(sql_script):
    operations = []
    lines = sql_script.splitlines()

    parsed = parse(sql_script)

    for statement in parsed:
        if statement.get_type() == 'INSERT':
            operations += extract_insert_target_with_line(statement, lines)
            operations += extract_from_join_tables_with_line(statement, lines, statement.get_type())
        elif statement.get_type() == 'SELECT':
            operations += extract_from_join_tables_with_line(statement, lines, statement.get_type())
        elif statement.get_type() == 'UPDATE':
            operations += extract_update_target_with_line(statement, lines)
            operations += extract_from_join_tables_with_line(statement, lines, statement.get_type())
        elif statement.get_type() == 'DELETE':
            operations += extract_delete_target_with_line(statement, lines)
            operations += extract_from_join_tables_with_line(statement, lines, statement.get_type())

    return operations

def extract_insert_target_with_line(statement, lines):
    operations = []
    for token in statement.tokens:
        if token.ttype == tokens.Keyword and token.value.upper() == 'INTO':
            table_token = statement.token_next(statement.token_index(token))
            if isinstance(table_token, sql.Identifier):
                operations.append(create_operation('INSERT', 'None', table_token.get_real_name(), find_line_number(token, lines), str(token).strip()))
            elif isinstance(table_token, sql.IdentifierList):
                for identifier in table_token.get_identifiers():
                    operations.append(create_operation('INSERT', 'None', identifier.get_real_name(), find_line_number(identifier, lines), str(token).strip()))
    return operations

def extract_from_join_tables_with_line(statement, lines, statement_type):
    operations = []
    from_seen = False
    join_keywords = {'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN', 'OUTER JOIN', 'CROSS JOIN'}

    for token in statement.tokens:
        if token.ttype == tokens.Keyword and token.value.upper() == 'FROM':
            from_seen = True
        elif from_seen and token.ttype == tokens.Keyword and token.value.upper() in join_keywords:
            from_seen = True
        elif from_seen and token.ttype == tokens.Keyword and token.value.upper() not in join_keywords:
            from_seen = False

        if from_seen:
            if isinstance(token, sql.Identifier):
                operations.append(create_operation(statement_type, token.get_real_name(), 'None', find_line_number(token, lines), str(token).strip()))
            elif isinstance(token, sql.IdentifierList):
                for identifier in token.get_identifiers():
                    operations.append(create_operation(statement_type, identifier.get_real_name(), 'None', find_line_number(identifier, lines), str(token).strip()))
            elif token.ttype == tokens.Punctuation and token.value == ',':
                continue

        if isinstance(token, sql.Identifier) and from_seen:
            operations.append(create_operation('JOIN', token.get_real_name(), 'None', find_line_number(token, lines), str(token).strip()))
        elif isinstance(token, sql.IdentifierList) and from_seen:
            for identifier in token.get_identifiers():
                operations.append(create_operation('JOIN', identifier.get_real_name(), 'None', find_line_number(identifier, lines), str(token).strip()))

    return operations

def extract_update_target_with_line(statement, lines):
    operations = []
    for token in statement.tokens:
        if isinstance(token, sql.Identifier):
            operations.append(create_operation('UPDATE', token.get_real_name(), 'None', find_line_number(token, lines), str(token).strip()))
    return operations

def extract_delete_target_with_line(statement, lines):
    operations = []
    for token in statement.tokens:
        if token.ttype == tokens.Keyword and token.value.upper() == 'FROM':
            table_token = statement.token_next(statement.token_index(token))
            if isinstance(table_token, sql.Identifier):
                operations.append(create_operation('DELETE', table_token.get_real_name(), 'None', find_line_number(table_token, lines), str(token).strip()))
            elif isinstance(table_token, sql.IdentifierList):
                for identifier in table_token.get_identifiers():
                    operations.append(create_operation('DELETE', identifier.get_real_name(), 'None', find_line_number(identifier, lines), str(token).strip()))
    return operations

def create_operation(sql_type, source_table, target_table, line_number, line_content):
    return {
        'sql_type': sql_type,
        'source_table': source_table,
        'target_table': target_table,
        'line_number': line_number,
        'line_content': line_content
    }

def find_line_number(token, lines):
    token_str = str(token).strip().lower()
    for i, line in enumerate(lines):
        if token_str in line.strip().lower():
            return i + 1
    return None

def main():
    path = "/corp/capital/saberconnect/calcs/counterparty/setup/sql_templates/"
    files = list(sandra.pathWalk(path, sandra.srcdb))
    results = []

    for i, sql_script_path in enumerate(files):
        sql_raw = sandra.srcdb.read(sql_script_path).content.get('text')
        operations = extract_tables_with_line_numbers(sql_raw)

        for operation in operations:
            results.append({
                's_no': i + 1,
                'script_path': sql_script_path,
                **operation
            })

    # Print results in tabular format
    print(f"{'S.No.':<5} {'Script Path':<60} {'SQL Type':<15} {'Source Table':<25} {'Target Table':<25} {'Line Number':<15} {'Line Content':<60}")
    for result in results:
        print(f"{result['s_no']:<5} {result['script_path']:<60} {result['sql_type']:<15} {result['source_table']:<25} {result['target_table']:<25} {result['line_number']:<15} {result['line_content']:<60}")

if __name__ == "__main__":
    main()

