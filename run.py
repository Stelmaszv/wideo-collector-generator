import json
from json import JSONDecodeError
from core.init import ValidJson,LoopRun,CreateDist
from core.settings import settings_array
from pathlib import Path
CreateDist()
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

from core.dir import ScanDirs
from core.config import ConfigModule
from core.websrabermodule import WebScraperModule

moduls = [
    {
        "obj": ScanDirs(data_json_dirs), "method": 'start',
        "stan": settings_array["scan_dir"], "start_mes": 'Scaning Dir ... Start', "end_mees": 'End scaning Dir ... OK',
    },

    {
        "obj":  ConfigModule(), "method": 'start',
        "stan": settings_array["config"], "start_mes": 'Config Dir ... Start', "end_mees": 'End config Dir ... OK',
    },

    {
        "obj": WebScraperModule(), "method": 'start',
        "stan": settings_array["scraper"], "start_mes": 'WebSraber ... Start', "end_mees": 'End of WebSraber ... ok',
    }
]

if __name__=="__main__":
    LR = LoopRun(moduls)
    LR.loop()