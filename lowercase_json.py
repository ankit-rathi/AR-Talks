import json

def lowercase_json(json_obj):
    """
    Convert all values in a JSON object to lowercase.
    
    Args:
        json_obj (dict): The JSON object.
        
    Returns:
        dict: A new JSON object with values converted to lowercase.
    """
    lowercase_obj = {}
    for key, value in json_obj.items():
        if isinstance(value, str):
            lowercase_obj[key] = value.lower()
        else:
            lowercase_obj[key] = value  # Preserve other types unchanged
    return lowercase_obj

# Example usage:
json_data = {
    "Name": "John",
    "Age": 30,
    "Email": "john@example.com",
    "City": "New York",
    "Country": "USA"
}

lowercase_data = lowercase_json(json_data)
print(lowercase_data)
