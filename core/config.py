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
    FactoryConfig=None

    def __init__(self,index):
        self.index=index

    def start_config(self):
        print(self.config_mess)
        for el in db[self.index]:
            if db[self.index][el]['config']=='False':
                self.FactoryConfig(el).config

class AbstractConfig(ABC):

    def __init__(self, index):
        self.index = index
        print(self.index)

    def config(self):
        print(self.index)

class ConfigStar(AbstractConfig):

    pass

class ConfigSeries(AbstractConfig):

    pass

class ConfigProducents(AbstractConfig):

    pass

class ConfigMovies(AbstractConfig):

    pass

class ConfigStarDir(AbstractDirConfig):
    FactoryConfig = ConfigStar
    config_mess = 'Config Stars ... Start'

class ConfigSeriesDir(AbstractDirConfig):
    FactoryConfig = ConfigSeries
    config_mess = 'Config Series ... Start'

class ConfigProducentsDir(AbstractDirConfig):
    FactoryConfig = ConfigProducents
    config_mess = 'Config Producents ... Start'

class ConfigMoviesDir(AbstractDirConfig):
    FactoryConfig = ConfigMovies
    config_mess = 'Config Movies ... Start'


