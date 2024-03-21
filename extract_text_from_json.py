import json
import os

def extract_text_from_json(input_location, json_file, key, output_location):
    # Construct the full path to the JSON file
    json_file_path = os.path.join(input_location, json_file)

    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print("JSON file does not exist.")
        return

    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract text based on the specified key
    text = data.get(key, '')

    # Check if text is empty
    if not text:
        print("No text found for the specified key.")
        return

    # Construct the full path for the output text file
    output_text_file = os.path.join(output_location, f"{key}.txt")

    # Save extracted text to text file
    with open(output_text_file, 'w') as file:
        file.write(text)

    print(f"Extracted text saved to {output_text_file}")

# Example usage
input_location = '/path/to/input/directory'  # Path to input directory containing JSON file
json_file = 'example.json'                    # JSON file name
key = 'text'                                  # Key to extract text from JSON
output_location = '/path/to/output/directory'  # Path to output directory to save the text file

extract_text_from_json(input_location, json_file, key, output_location)
