import json
from json import JSONDecodeError
from core.init import ValidJson,LoopRun,CreateDist
from core.settings import setings_array
from pathlib import Path
CreateDist()
from core.dir import ScanDirs
data_json_dirs={}
print("Validate data.JSON file ... Start")

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

moduls = [
    {
        "obj": ScanDirs(data_json_dirs), "method": 'start',
         "stan": setings_array["scan_dir"], "start_mes": 'Scaning Dir ... Start', "end_mees": 'Scaning Dir ... OK'
    },
]

LR=LoopRun(moduls)
LR.loop()