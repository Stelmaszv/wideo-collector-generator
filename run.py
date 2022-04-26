import json
from json import JSONDecodeError
from core.init import ValidJson,get_data_from_json
from pathlib import Path
data_json_dirs={}
print("Validate data.JSON file ...")
if Path('data.json').is_file():
    try:
        with open('data.json') as f:
            data = json.load(f)
            data_JSON = data
            VJ = ValidJson(data_JSON)
            VJ.valid()
            data_json_dirs=VJ.set_dirs(data_json_dirs)
    except JSONDecodeError:
        exit('Validate data.JSON file ... Invalid File data.JSON file !')
else:
    exit('Validate data.JSON file ... Please Create File data.JSON !')
