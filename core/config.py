import ast
import json
import os
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

        os.remove("dist.json")
        a_file = open("dist.json", "w")
        json.dump(db, a_file)
        a_file.close()

class AbstractDirConfig(ABC):

    config_mess=''
    FactoryConfig=None

    def __init__(self,index):
        self.index=index

    def start_config(self):
        print(self.config_mess)
        for el in db[self.index]:
            if db[self.index][el]['config']=='False':
                self.FactoryConfig(self.index,el).config()

class AbstractConfig(ABC):

    forbiten_fields=['name','dir','config']

    def __init__(self,index,element):
        self.index=index
        self.element = element

    def on_config(self):
        pass

    def config(self):

        print('Config ... '+self.element)

        with open(db[self.index][self.element]['dir']+'/config.JSON') as f:
            data = json.load(f)
            self.on_config(data,db[self.index][self.element])
            for el in data:
                if el not in self.forbiten_fields:
                    db[self.index][self.element][el]=data[el]

class ConfigStar(AbstractConfig):

    def on_config(self,data,index):
        pass

class ConfigSeries(AbstractConfig):

    def on_config(self, data, index):
        pass

class ConfigProducents(AbstractConfig):

    def on_config(self, data, index):
        pass

class ConfigMovies(AbstractConfig):

    def on_config(self, data, index):
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


