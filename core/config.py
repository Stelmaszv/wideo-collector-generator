import ast
from abc import ABC, abstractmethod
with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class ConfigModule:

    def start(self):
        config_dirs= {
            "series"  :ConfigSeriesDir,
            "movies" :ConfigMoviesDir,
            "stars": ConfigStarDir,
            "producents":ConfigProducentsDir
        }

        for dir in db:
            config_dirs[dir](dir).start_config()

class AbstractDirConfig(ABC):

    config_mess=''

    def __init__(self,index):
        self.index=index

    def start_config(self):
        print(self.config_mess)
        for el in db[self.index]:
            pass

class ConfigStarDir(AbstractDirConfig):
    config_mess = 'Config Stars ... Start'

class ConfigSeriesDir(AbstractDirConfig):
    config_mess = 'Config Series ... Start'

class ConfigProducentsDir(AbstractDirConfig):
    config_mess = 'Config Producents ... Start'

class ConfigMoviesDir(AbstractDirConfig):
    config_mess = 'Config Movies ... Start'


