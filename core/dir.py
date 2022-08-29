import os
import json
import ast
import re
from abc import ABC, abstractmethod
from os.path import exists
from pathlib import Path

import setuptools.command.easy_install

from core.settings import movie_ext

if Path('dist.json').is_file():
    with open('dist.json') as f:
        data = f.read()
        db = ast.literal_eval(data)

class FaindStar:

    str = ''
    starArray=[]

    def __init__(self,dir):
        self.dir=dir
        self.start = self.dir.find("(")
        self.end = self.dir.find(")")

    def return_stars_in_string(self):
        str=''
        for i in range(self.start+1,self.end):
            str=str+self.dir[i]
        return str

    def create_star_list(self):
        str=self.return_stars_in_string()
        self.starArray = str.split(' and ')
        return self.starArray

class ScanDirs:

    def __init__(self,dir):
        self.dir = dir

    def start(self):
        scan_dir= {
            "stars"  :StarsDir,
            "series" :SeriesDir,
            "producents": ProducentsDir,
        }
        for dir in self.dir:
            if dir != "movies":
                print('Scaning Dir ... Dir '+dir+'')
                dir=scan_dir[dir](self.dir[dir])
                dir.scan()

class AbstractScan(ABC):
    base_dir=['A-D','E-H','I-L','M-P','R-U','W-Z']
    FactoryScan = None

    def __init__(self,dir):
        self.dir=dir
        self.base_init_dir()

    def scan(self):
        dir_list = os.listdir(self.dir)
        for dir in dir_list:
            is_dir = os.path.isdir(self.dir + '\\' + dir)
            if is_dir:
                dir_list_elemnts = os.listdir(self.dir + '\\' + dir)
                for el in dir_list_elemnts:
                    self.FactoryScan(self.dir + '\\' + dir + '\\' + el).scan()
        os.remove("dist.json")
        a_file = open("dist.json", "w")
        json.dump(db, a_file)
        a_file.close()

    def init_dir(self):
        self.base_init_dir()

    def base_init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir+'\\'+dir) is False:
                os.mkdir(self.dir+'\\'+dir)

class BasseScan:
    shema_url=''
    base_dir=[]
    wrong_string=["'"," "]

    def base_init(self,name,dir):
        self.name = name
        print('Adding ... ' + self.name + '')
        self.dir = dir + '\\' + self.name

    def escepe_string(self,name):
        return name.replace(' ','-')

    def create_json_config(self):
        if exists(self.dir + '\\config.json') is False:
            f = open(self.dir + '\\config.json', "x")
            f.write(Path(self.shema_url).read_text())
            f.close()
            return True
        return False

    """
    def convert(self,a):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct
    """

    def clear_name(self,name):
        str = ''
        stop = False
        for i in range(0, len(name)):

            if name[i] == "[":
                stop = True

            if name[i] == "(":
                stop = True

            if name[i] == ".":
                stop = True

            if stop is False:
                str = str + name[i]

        if str[len(str) - 1] == ' ':
            nstr = ''
            for i in range(0, len(str) - 1):
                if i < len(str) - 1:
                    nstr = nstr + str[i]
            return nstr
        return str

    def set_dir(self, name,star_dir):
        from core.defs import set_dir
        from run import data_json_dirs
        return set_dir(name,data_json_dirs[star_dir])

    def init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir + '\\' + dir) is False:
                os.makedirs(self.dir + '\\' + dir)

class AbstractAddElment(ABC,BasseScan):

    shema_url = 'json_schema/movies.JSON'

    def __init__(self,name,dir=''):
        print(name,dir)
        self.base_init(name,dir)
        self.create_dir()

    def create_dir(self):
        print(os.path.isdir(self.dir))
        if os.path.isdir(self.dir) is False:
            os.makedirs(self.dir)
        db['movies'][self.name]['dir'] = self.dir
        self.create_json_config()

    @abstractmethod
    def add(self):
        pass

    def return_test_db(self):
        return self.test_db

class StarElment(AbstractAddElment):

    base_dir = ['movies', 'photos']
    shema_url = 'json_schema/star.JSON'

    def __init__(self, name, dir='',test_db={}):
        self.test_db=test_db
        self.base_init(name,dir)
        self.create_dir()
        self.create_json_config()
        self.init_dir()
        try:
            db['stars'][name] = {'name': name, 'config': str(False),'dir':self.dir}
            self.test_db=db
        except:
            self.test_db['stars'][name] = {'name': name, 'config': str(False), 'dir': self.dir}

    def create_dir(self):
        self.dir=self.set_dir(self.name,'stars')
        if os.path.isdir(self.dir) is False:
            os.makedirs(self.dir)

    def add(self):
        pass

class MovieElment(AbstractAddElment):

    validValue = "[a-zA-Z0-9]+\s+\([a-zA-Z0-9\s]+\)";

    def add_stars(self,stars):
        stars_dist={}
        if stars is not None:
            for star in stars:
                stars_dist[star]={"star_name":star}
        return stars_dist

    def get_dir(self):
        return self.dir;

    def add(self):
        stars = self.faind_stars(db['movies'][self.name]['full_name'])
        db['movies'][self.name]['stars'] = self.add_stars(stars)
        self.add_stars_in_movie_to_db(stars)

    def add_stars_in_movie_to_db(self,stars):
        if stars is not None:
            for star in stars:
                StarElment(star).add()

    def faind_stars(self, file):
        FS = FaindStar(file)
        if re.search(self.validValue, file):
            string = FS.return_stars_in_string()
            return FS.create_star_list()
        return None

class AbstractScanElement(ABC,BasseScan):

    scan_dir= ''
    shema_url = ''
    ElmentFactory=MovieElment
    index=''

    def __init__(self,dir):
        self.dir = dir
        self.init_dir()
        self.create_json_config()
        self.name=self.get_name()
        print('Scaning Dir ... Dir ' + self.name + '')
        self.add_to_db()

    def get_name(self):
        dir=self.dir.split('\\')
        return  dir[len(dir)-1]
    def scan(self):
        dir_list = os.listdir(self.dir + '\\' + self.scan_dir);
        db[self.index][self.name]['movies'] = {}
        for dir in dir_list:
            is_dir = os.path.isdir(self.dir + '\\' + self.scan_dir + '\\' + dir)
            if is_dir:
                dir_list_el = os.listdir(self.dir + '\\' + self.scan_dir + '\\' + dir + '')
                for el_in_dir in dir_list_el:
                    if el_in_dir.endswith(movie_ext):

                        movie_dir = self.dir + '\\' + dir
                        new_movie_dir = movie_dir.replace("series", "movies")
                        db[self.index][self.name]['movies'][self.clear_name(el_in_dir)] = self.clear_name(el_in_dir)
                        db['movies'][self.clear_name(el_in_dir)] = {
                            'name': self.clear_name(el_in_dir),
                            'full_name': el_in_dir,
                            'dir': new_movie_dir,
                            'series': self.name,
                            'src': self.dir + '\\' + self.scan_dir + '\\' + dir + '\\' + self.clear_name(el_in_dir),
                            'config': str(False),
                            'season': dir,
                            'tags': {},
                        }
                        MovieElment(self.clear_name(el_in_dir), new_movie_dir).add()
                        self.action_after_index(db[self.index][self.name])
        self.create_scraber_list(db[self.index][self.name]['movies'])

    def action_after_index(self,elment):
        pass

    def create_scraber_list(self,list):
        elements={}
        for el in list:
            elements[el]=''

        location=db[self.index][self.name]['dir']+'/scraber_list.json';
        if os.path.exists(location) is False:
            a_file = open(location, "w")
            json.dump(elements, a_file)
            a_file.close()

    def add_to_db(self):
        db[self.index][self.name] = {'name': self.name, 'dir': self.dir, 'config': str(False)}
        self.db_el = db[self.index][self.name]

class ScanSerie(AbstractScanElement):

    scan_dir = 'movies'
    index = 'series'
    base_dir=['movies','photos','banners','stars','covers']
    db_el=''
    shema_url = 'json_schema/series.JSON'

class ScanStar(ScanSerie):

    index = 'stars'
    base_dir = ['movies', 'photos']
    shema_url = 'json_schema/star.JSON'

    def add_stars(self,nstars,stars):
        stars_dist={}
        for star in nstars:
            stars_dist[star]={"star_name":star}
        stars_dist.update(stars)
        return stars_dist

class ScanProducent(ScanSerie):

    base_dir = ['movies', 'photos', 'banners', 'stars']
    shema_url = 'json_schema/producent.JSON'
    index = 'producents'

class StarsDir(AbstractScan):
    FactoryScan = ScanStar

class SeriesDir(AbstractScan):
    FactoryScan = ScanSerie

class ProducentsDir(AbstractScan):
    FactoryScan = ScanProducent




