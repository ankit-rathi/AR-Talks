def replace_none_with_string(d):
    """
    Recursively replace None values in a dictionary with the string 'None'.
    
    :param d: Dictionary to be processed
    :return: Processed dictionary with 'None' strings instead of None values
    """
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursive call for nested dictionaries
            replace_none_with_string(value)
        elif value is None:
            d[key] = 'None'

# Example dictionary of dictionaries
example_dict = {
    'key1': {
        'subkey1': None,
        'subkey2': 'value2'
    },
    'key2': {
        'subkey1': 'value3',
        'subkey2': None
    },
    'key3': None
}

# Replace None with 'None'
replace_none_with_string(example_dict)

print(example_dict)
