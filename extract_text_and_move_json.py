import json
import os
import shutil

def extract_text_and_move_json(input_location, output_location, archive_location):
    # Iterate over each file in the input directory
    for json_file in os.listdir(input_location):
        # Check if the file is a JSON file
        if json_file.endswith('.json'):
            # Construct the full path to the JSON file
            json_file_path = os.path.join(input_location, json_file)

            # Read JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Extract text from JSON
            text = data.get('text', '')

            # Check if text is empty
            if not text:
                print(f"No text found in {json_file}.")
                continue

            # Construct the full path for the output text file
            output_text_file = os.path.join(output_location, f"{json_file.split('.')[0]}.txt")

            # Save extracted text to text file
            with open(output_text_file, 'w') as file:
                file.write(text)

            print(f"Extracted text from {json_file} saved to {output_text_file}")

            # Move processed JSON file to archive location
            archive_json_file_path = os.path.join(archive_location, json_file)
            shutil.move(json_file_path, archive_json_file_path)
            print(f"Processed JSON file {json_file} moved to {archive_json_file_path}")

# Example usage
input_location = '/path/to/input/directory'      # Path to input directory containing JSON files
output_location = '/path/to/output/directory'    # Path to output directory to save the text files
archive_location = '/path/to/archive/directory'  # Path to archive directory

extract_text_and_move_json(input_location, output_location, archive_location)
