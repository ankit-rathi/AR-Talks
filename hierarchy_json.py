def get_hierarchy_level(json_obj):
    def _get_level(obj, level):
        if isinstance(obj, dict):
            if not obj:
                return level
            return max(_get_level(v, level + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return level
            return max(_get_level(v, level + 1) for v in obj)
        else:
            return level

    return _get_level(json_obj, 0)

# Example usage:
import json

# Sample JSON object
json_data = {
    "key1": {
        "key2": 
            "abc"
        
    }
}

# Convert the JSON object to a Python dictionary
dict_data = json.loads(json.dumps(json_data))

# Get the hierarchy level
level = get_hierarchy_level(dict_data)
print("Hierarchy level:", level)
