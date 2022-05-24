import ast
import json
import os
from abc import ABC
from pathlib import Path

from core.dir import StarElment

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
    if_count_stars=False

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

    def count_stars(self):
        star_cunter={}
        for movie in db['movies']:
            if db['movies'][movie]['series'] ==  self.element:
                for star in db['movies'][movie]['stars']:
                    if star not in star_cunter.keys():
                        star_cunter[star]={
                            'name':star,
                            'counter':1
                        }
                    else:
                        star_cunter[star]['counter'] = star_cunter[star]['counter']+1
                        dir_location=db[self.index][self.element]['dir']+'\\stars\\'+star
                        if star_cunter[star]['counter'] >= 3 and os.path.isdir(dir_location) is False:
                            os.mkdir(dir_location)

    def config(self):
        print('Config ... '+self.element)
        with open(db[self.index][self.element]['dir']+'/config.JSON') as f:
            data = json.load(f)
            if self.if_count_stars:
                self.count_stars()
            data = self.on_config(data,db[self.index][self.element])
            for el in data:
                if el not in self.forbiten_fields and el in self.fields:
                    db[self.index][self.element][el]=data[el]
                else:
                    print('Warning ! Field '+el+' is invalid for '+self.index)

class ConfigStar(AbstractConfig):

    fields     = ['show_name','avatar']
    if_count_stars = False

    def on_config(self,data,index)->data:
        data['avatar'] = self.get_img('avatar')
        return data

class ConfigSeries(AbstractConfig):

    fields = ['show_name']
    if_count_stars = True

    def on_config(self, data, index):
        return data

class ConfigProducents(AbstractConfig):

    fields = ['show_name']
    if_count_stars = True

    def on_config(self, data, index):

        return data

class ConfigMovies(AbstractConfig):

    fields = ['show_name','poster','cover','stars']
    photo_dir = ''

    def add_stars(self,nstars,stars):
        stars_dist={}
        for star in nstars:
            stars_dist[star]={"star_name":star}
            StarElment(star).add()
        stars_dist.update(stars)
        return stars_dist

    def on_config(self, data, index):
        data['cover'] = self.get_img('cover')
        data['cover'] = self.get_img('cover')

        if "stars" in data:
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


