import ast
from abc import ABC, abstractmethod
with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class ConfigModule:

    def start(self):
        config_dirs= {
            "series"  :ConfigSeriesDir,
            "movies" :ConfigSeriesDir,
            "stars": ConfigStarDir,
            "producents":ConfigProducentsDir
        }

        for dir in db:
            config_dirs[dir](dir).start_config()

class AbstractDirConfig(ABC):

    def __init__(self,index):
        print(index)

    @abstractmethod
    def start_config(self):
        pass

class ConfigStarDir(AbstractDirConfig):
    def start_config(self):
        print('ConfigStarDir')

class ConfigSeriesDir(AbstractDirConfig):
    def start_config(self):
        print('ConfigSeriesDir')

class ConfigProducentsDir(AbstractDirConfig):
    def start_config(self):
        print('ProducentsDir')

