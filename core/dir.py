import os
import json
import pickle
import ast
import re
from abc import ABC, abstractmethod
from pathlib import Path
from core.settings import movie_ext

with open('D:\project\wideo-collector-generator\dist.json') as f:
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

    def create_json_config(self):
        if Path(self.dir + '\\config.json').is_file() is False:
            f = open(self.dir + '\\config.json', "x")
            f.write(Path(self.shema_url).read_text())
            f.close()

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

class AbstractAddElment(ABC,BasseScan):

    shema_url = 'json_schema/movies.JSON'

    def __init__(self,name,dir):
        self.name=name
        print('Adding ... ' + self.name + '')
        self.dir = dir + '\\' + self.name
        self.create_dir()

    def create_dir(self):
        if os.path.isdir(self.dir) is False:
            os.makedirs(self.dir)
        db['movies'][self.name]['dir'] = self.dir
        self.create_json_config()

    @abstractmethod
    def add(self):
        pass

class MovieElment(AbstractAddElment):

    validValue = "[a-zA-Z0-9]+\s+\([a-zA-Z0-9\s]+\)";

    def add(self):
        self.stars = self.faind_stars(self.name)

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

    def __init__(self,dir):
        self.dir = dir
        self.init_dir()
        self.create_json_config()
        self.name=self.get_name()
        print('Scaning Dir ... Dir ' + self.name + '')
        self.add_to_db()

    def get_name(self):
        return  self.dir.split('\\')[4]

    @abstractmethod
    def scan(self):
        pass

    def add_to_db(self):
        pass

    def init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir + '\\' + dir) is False:
                os.makedirs(self.dir + '\\' + dir)


class ScanSerie(AbstractScanElement):

    scan_dir = 'movies'
    base_dir=['movies','photos\\DATA','banners','stars']
    db_el=''
    shema_url = 'json_schema/series.JSON'

    def scan(self):
        dir_list = os.listdir(self.dir + '\\' + self.scan_dir);
        for dir in dir_list:
            is_dir = os.path.isdir(self.dir + '\\' + self.scan_dir + '\\' + dir)
            if is_dir:
                dir_list_el = os.listdir(self.dir + '\\' + self.scan_dir + '\\' + dir+'\\DATA')
                for el_in_dir in dir_list_el:
                    if el_in_dir.endswith(movie_ext):
                        movie_dir=self.dir+'\\'+dir
                        new_movie_dir=movie_dir.replace("series", "movies")
                        db['movies'][self.clear_name(el_in_dir)]={
                            'name':self.clear_name(el_in_dir),
                            'dir':new_movie_dir,
                            'src':self.dir + '\\' + self.scan_dir + '\\' + dir+'\\DATA\\'+el_in_dir
                        }
                        MovieElment(self.clear_name(el_in_dir),new_movie_dir).add()


    def add_to_db(self):
        db['series'][self.name]={'name':self.name,'dir':self.dir}
        self.db_el=db['series'][self.name]

class ScanStar(AbstractScanElement):

    def scan(self):
        pass

class ScanProducent(AbstractScanElement):

    def scan(self):
        pass

class StarsDir(AbstractScan):
    FactoryScan = ScanStar

class SeriesDir(AbstractScan):
    FactoryScan = ScanSerie

class ProducentsDir(AbstractScan):
    FactoryScan = ScanProducent




