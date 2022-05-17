import ast
import json
import os
from abc import ABC
from pathlib import Path
with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class ConfigModule:

    def __int__(self):
        print('init')

    def start(self):
        config_dirs= {
            "series"  :ConfigSeriesDir,
            "movies" :ConfigMoviesDir,
            "stars": ConfigStarDir,
            "producents":ConfigProducentsDir
        }
        for dir in db:
            config_dirs[dir](dir).start_config()
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
    fields = []
    photo_dir = 'photos'

    def __init__(self,index,element):
        self.index=index
        self.element = element

    def get_img(self,name):
        photo_list=db[self.index][self.element]['dir']+'\\'+self.photo_dir
        for photo in os.listdir(photo_list):
            if name==Path(photo).stem:
                return db[self.index][self.element]['dir']+'\\'+self.photo_dir+'\\'+photo
        return ''

    def on_config(self,data,index)->data:
        return data

    def config(self):

        print('Config ... '+self.element)

        with open(db[self.index][self.element]['dir']+'/config.JSON') as f:
            data = json.load(f)
            data = self.on_config(data,db[self.index][self.element])
            for el in data:
                if el not in self.forbiten_fields and el in self.fields:
                    db[self.index][self.element][el]=data[el]
                else:
                    print('Warning ! Field '+el+' is invalid for '+self.index)

class ConfigStar(AbstractConfig):

    fields     = ['show_name','avatar']

    def on_config(self,data,index)->data:
        data['avatar'] = self.get_img('avatar')
        return data

class ConfigSeries(AbstractConfig):

    fields = ['show_name']

    def on_config(self, data, index):
        return data

class ConfigProducents(AbstractConfig):

    fields = ['show_name']

    def on_config(self, data, index):

        return data

class ConfigMovies(AbstractConfig):

    fields = ['show_name','poster','cover','stars']
    photo_dir = ''

    def add_stars(self,nstars,stars):
        stars_dist={}
        for star in nstars:
            stars_dist[star]={"star_name":star}
        stars_dist.update(stars)
        return stars_dist

    def on_config(self, data, index):
        data['poster'] = self.get_img('poster')
        data['cover']  = self.get_img('cover')
        data['stars']  = self.add_stars(data['stars'],index['stars'])
        return data

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


