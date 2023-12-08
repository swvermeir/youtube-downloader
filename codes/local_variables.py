import json
import os
local_json = "local_variables.json"


def write_json(data, file: str = local_json):
    with open(file, 'w') as f:
        json.dump(data, f)


def read_json(file: str = local_json):
    if not os.path.exists(file):
        return None
    
    with open(file, 'r') as f:
        return json.load(f)
