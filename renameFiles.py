import os
import json
import time
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
                    
                    # Try to rename the file with retries
                    max_retries = 5
                    for attempt in range(max_retries):
                        try:
                            os.rename(file_path, new_file_path)
                            print(f"Renamed '{filename}' to '{new_filename}'")
                            break  # Exit retry loop if successful
                        except PermissionError:
                            if attempt < max_retries - 1:  # Don't wait on the last attempt
                                print(f"File '{filename}' is in use. Retrying...")
                                time.sleep(1)  # Wait before retrying
                            else:
                                print(f"Failed to rename '{filename}' after {max_retries} attempts.")
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")

# Example usage
folder_path = 'PIEJSONS'
rename_json_files(folder_path)
