import os
import json
from datetime import datetime

def rename_json_files(folder_path):
    # Get the current date in the required format
    current_date_formatted = datetime.now().strftime("%m-%d-%y")
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Read the JSON content
            content = None
            try:
                with open(file_path, 'r') as file:
                    content = json.load(file)
                    # Extract the weekOf date
                week_of_str = content["metadata"]["Parameters"]["weekOf"]
                
                # Convert weekOf string to datetime object
                week_of_date = datetime.fromisoformat(week_of_str[:-1])  # remove 'Z' and convert
                
                # Format the week_of date
                week_of_formatted = week_of_date.strftime("%m-%d-%y")
                
                # Create the new filename
                new_filename = f"{week_of_formatted}_{current_date_formatted}.json"
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Only rename if the new file path does not already exist
                if not os.path.exists(new_file_path):
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"File '{new_filename}' already exists. Skipping renaming for '{filename}'.")
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")
            except PermissionError:
                print(f"Permission error with file '{filename}'. Skipping...")

# Example usage



# Example usage
def check_file_accessibility(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as file:
                    file.read()  # Try to read the file
            except Exception as e:
                print(f"Cannot access '{filename}': {e}")

# Example usage
folder_path = 'PIEJSONS'
check_file_accessibility(folder_path)

rename_json_files(folder_path)
