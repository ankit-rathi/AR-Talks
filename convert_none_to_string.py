import json

def convert_none_to_string(data):
    if isinstance(data, list):
        return [convert_none_to_string(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_none_to_string(value) for key, value in data.items()}
    elif data is None:
        return 'None'
    else:
        return data

# Example usage
json_list = [
    {"name": "Alice", "age": None, "city": "New York"},
    {"name": "Bob", "age": 30, "city": None},
    None,
    "string",
    123,
    [None, {"key": None}]
]

converted_list = convert_none_to_string(json_list)
print(json.dumps(converted_list, indent=2))
