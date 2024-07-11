import re

def check_special_characters(request_params, valid_special_chars="._-"):
    """
    Check if any of the request parameters contain special characters, except for valid ones.

    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    valid_special_chars (str): String of valid special characters. Default is "._-".

    Returns:
    bool: True if any parameter contains invalid special characters, False otherwise.
    """
    # Create a regex pattern to match invalid characters
    invalid_chars_pattern = re.compile(f"[^{re.escape(valid_special_chars)}a-zA-Z0-9]")

    keys_with_invalid_special_chars = []
    for key, value in request_params.items():
        if isinstance(value, str) and invalid_chars_pattern.search(value):
            keys_with_invalid_special_chars.append(key)
    return keys_with_invalid_special_chars

# Example usage:
params = {
    "param1": "valid_value",
    "param2": "invalid@value",
    "param3": "another.valid-value"
}

print(check_special_characters(params))  # Output: True
