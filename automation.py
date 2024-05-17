import os
import re
import csv

def search_variable_usage(folder_path, variable_names):
    results = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.py') or file_name.endswith('.sql'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    func_name = None
                    for line_num, line in enumerate(lines, start=1):
                        if "def " in line:
                            # Extract the function name
                            func_name = re.findall(r'def\s+(\w+)\s*\(', line)
                            func_name = func_name[0] if func_name else None
                        if func_name and "return" in line:
                            func_name = None  # Reset after return statement

                        for var_name in variable_names:
                            pattern = r'\b{}\b'.format(var_name)
                            if re.search(pattern, line):
                                # Identify usage and impact
                                if func_name:
                                    use_case = f"{func_name}-function"
                                else:
                                    use_case = "variable assignment" if "=" in line else "other usage"
                                # Add details to results
                                results.append((file_path, var_name, use_case, line_num))
                                # Reset function name tracking if it is within a function
                                if use_case.endswith("-function"):
                                    func_name = None

    return results

def write_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['scriptpath', 'column_name', 'impact_area', 'linenumber']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({'scriptpath': result[0], 'column_name': result[1], 'impact_area': result[2], 'linenumber': result[3]})

if __name__ == "__main__":
    # Get the current working directory
    current_directory = os.getcwd()

    # Append the given directory path to the current working directory
    given_directory = input("Enter the folder path: ")  # Prompt user to enter the folder path
    full_directory_path = os.path.join(current_directory, given_directory)

    # Specify the variable names to search for
    variable_names = ['gl_account', 'company', 'costcenter']  # Add more variable names if needed

    # Specify the output file name
    output_file = 'variable_impact.csv'

    # Search for variable usage in Python and SQL files within the specified directory
    results = search_variable_usage(full_directory_path, variable_names)

    # Write the results to a CSV file
    write_results_to_csv(results, output_file)
