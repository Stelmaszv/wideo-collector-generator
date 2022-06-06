import ast
import json
import os
from abc import ABC
from pathlib import Path
from core.defs import set_dir
from core.dir import StarElment, ScanSerie
from core.settings import ethnicity,hair_color
from core.helper import DataValid

with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class ConfigModule:

    def start(self):
        config_dirs= {
            "series"  :ConfigSeriesDir,
            "movies" :ConfigMoviesDir,
            "stars": ConfigStarDir,
            "producents":ConfigProducentsDir,
        }
        for dir in db:
            if dir != "tags":
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
                self.FactoryConfig(self.index,el).config()

class AbstractConfig(ABC):

    forbiten_fields=['name','dir','config','src','full_name','season']
    fields = []
    photo_dir = 'photos'
    if_count_stars=False

    def __init__(self,index,element):
        self.index=index
        self.element = element

    def get_img(self,name,defult):
        photo_list=db[self.index][self.element]['dir']+'\\'+self.photo_dir
        for photo in os.listdir(photo_list):
            if name==Path(photo).stem:
                return db[self.index][self.element]['dir']+'\\'+self.photo_dir+'\\'+photo
        return defult

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
    def add_tags(self,tags):
        def valid_tags(tags):
            valid_tags_return=[]
            for tag in tags:
                tag = tag.capitalize()
                valid_tags_return.append(tag)
            return valid_tags_return

        tags_valid=valid_tags(tags)
        tag_dist = {}
        for tag in tags_valid:
            tag_dist[tag] = {"tag_name": tag}
        db['tags'].update(tag_dist)
        return {'tags':tag_dist}

    def valid_number(self,number,limit):
        return (number > limit)

    def if_value_is_valid_array(self,value,array,error):
        if value:
            if value in array:
                return value
            else:
                print(error)
                return False
        return False

    def valid_data(self,data,to_today=False):
        if data!='YEAR-MOUNT-DAY':
            DV=DataValid()
            DV.set_data(data,to_today,db[self.index][self.element],self.index)
            return DV.is_valid()

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

        os.remove("dist.json")
        a_file = open("dist.json", "w")
        json.dump(db, a_file)
        a_file.close()

        a_file = open(db[self.index][self.element]['dir']+"/config.JSON", "w")
        json.dump(data, a_file)
        a_file.close()

class ConfigStar(AbstractConfig):

    fields     = ['show_name','avatar','tags','hair_color','description','weight',
                  'height','ethnicity','hair_color','birth_place','nationality',
                  'date_of_birth','scraper']
    if_count_stars = False

    def on_config(self,data,index)->data:
        data['avatar'] = self.get_img('avatar',data['avatar'])

        if "tags" in data:
            data['tags']  = self.add_tags(data['tags'])

        if self.valid_number(data['weight'],0):
            pass

        if self.valid_number(data['height'],0):
            pass

        if self.if_value_is_valid_array(data['ethnicity'],ethnicity,'Invalid Ethnicity'):
            pass

        if self.if_value_is_valid_array(data['hair_color'],hair_color,'Invalid hair_color'):
            pass

        if self.valid_data(data['date_of_birth'],True):
            pass
        return data

class ConfigSeries(AbstractConfig):

    fields = ['show_name','producent','tags','avatar','number_of_sezons',
              'description','country','years','scraper']
    if_count_stars = True

    def add_producent(self,producent):
        from run import data_json_dirs
        producent_dist={}
        producent_dist['producent']={"series_name":producent}
        start = data_json_dirs['producents']
        set_location= set_dir(producent,start)
        ScanSerie(set_location)
        return producent_dist

    def number_of_sezons(self):
        location=db[self.index][self.element]['dir']+'\\movies'
        return len(os.listdir(location))

    def on_config(self, data, index):
        self.count_stars()
        data['number_of_sezons'] = self.number_of_sezons()
        data['avatar']=self.get_img('avatar',data['avatar'])

        if "producent" in data:
            data['producent']  = self.add_producent(data['producent'])

        if "tags" in data:
            data['tags']  = self.add_tags(data['tags'])

        return data

class ConfigProducents(AbstractConfig):

    fields = ['show_name','series','tags','description','country','avatar','scraper']
    if_count_stars = True

    def add_series(self,series):
        from run import data_json_dirs
        series_dist={}
        for serie in series:
            series_dist[serie]={"series_name":serie}
            start = data_json_dirs['series']
            set_location= set_dir(serie,start)
            ScanSerie(set_location)
        return series_dist

    def on_config(self, data, index):
        data['avatar'] = self.get_img('avatar', data['avatar'])
        if "series" in data:
            data['series']  = self.add_series(data['series'])

        if "tags" in data:
            data['tags']  = self.add_tags(data['tags'])

        return data

class ConfigMovies(AbstractConfig):

    fields = ['show_name','poster','cover','stars','tags','description',
              'country','date_relesed','scraper']
    photo_dir = ''

    def add_stars(self,nstars,stars):
        stars_dist={}
        for star in nstars:
            stars_dist[star]={"star_name":star}
            StarElment(star).add()
        stars_dist.update(stars)
        return stars_dist

    def find_cover(self,cover):
        dir=os.listdir(db['series'][db[self.index][self.element]['series']]['dir']+'\\covers')
        for photo in dir:
            if cover==Path(photo).stem:
                return db['series'][db[self.index][self.element]['series']]['dir']+'\\covers\\'+photo

    def on_config(self, data, index):
        data['cover']=self.get_img('cover',data['cover'])
        data['poster']=self.get_img('poster',data['poster'])
        cover_srt=data['cover'].split(':')
        if len(cover_srt)>0 and cover_srt[0]=="get":
            data['cover']=self.find_cover(cover_srt[1])

        if len(cover_srt) > 0 and cover_srt[0] == "getseason":
            data['cover'] = self.find_cover('season_' + index['season'])

        if "stars" in data:
            data['stars']  = self.add_stars(data['stars'],index['stars'])

        if "tags" in data:
            data['tags']  = self.add_tags(data['tags'])

        if self.valid_data(data['date_relesed']):
            pass
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


