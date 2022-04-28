import os
import json
import pickle
import ast
from abc import ABC, abstractmethod
from pathlib import Path
from core.settings import movie_ext

with open('D:\project\wideo-collector-generator\dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

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

class AbstractAddElment(ABC):

    def __init__(self,name):
        self.name=name
        print('Adding ... ' + self.name + '')

    @abstractmethod
    def add(self):
        pass

class MovieElment(AbstractAddElment):

    def add(self):
        pass

class AbstractScanElement(ABC):

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

    def create_json_config(self):
        if Path(self.dir + '\\config.json').is_file() is False:
            f = open(self.dir + '\\config.json', "x")
            f.write(Path(self.shema_url).read_text())
            f.close()

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
                        db['movies'][el_in_dir]={'series':self.name}
                        MovieElment(el_in_dir).add()


    def add_to_db(self):
        db['series'][self.name]={'name':self.name}
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




