import os
import re
import csv

def get_current_script_path():
    # Get the current script's full path
    script_path = os.path.abspath(__file__)
    print(f"The full path of the currently executing script is: {script_path}")
    return script_path

def search_variable_usage(folder_path, variable_names):
    results = []

    if not os.path.exists(folder_path):
        print(f"Error: The path {folder_path} does not exist.")
        return results

    print(f"Searching in folder: {folder_path}")

    for root, dirs, files in os.walk(folder_path):
        print(f"Exploring: {root}")
        print(f"Directories: {dirs}")
        print(f"Files: {files}")
        for file_name in files:
            if file_name.endswith('.py') or file_name.endswith('.sql'):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")
                try:
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
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return results

def write_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['scriptpath', 'column_name', 'impact_area', 'linenumber']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({'scriptpath': result[0], 'column_name': result[1], 'impact_area': result[2], 'linenumber': result[3]})

if __name__ == "__main__":
    # Get the path of the currently executing script
    current_script_path = get_current_script_path()

    # Derive the directory containing the current script
    script_directory = os.path.dirname(current_script_path)

    print(f"Derived script directory: {script_directory}")

    # Ensure the script directory exists
    if not os.path.exists(script_directory):
        print(f"Error: The path {script_directory} does not exist or is not accessible.")
    else:
        # Specify the variable names to search for
        variable_names = ['gl_account', 'company', 'costcenter']  # Add more variable names if needed

        # Specify the output CSV file path
        output_file = os.path.join(script_directory, "output.csv")

        # Search for variable usage in Python and SQL files within the script directory
        results = search_variable_usage(script_directory, variable_names)

        # Write the results to a CSV file
        write_results_to_csv(results, output_file)

        print(f"Results written to {output_file}")
