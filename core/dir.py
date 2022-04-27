import os
from abc import ABC, abstractmethod
from pathlib import Path

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

    def init_dir(self):
        self.base_init_dir()

    def base_init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir+'\\'+dir) is False:
                os.mkdir(self.dir+'\\'+dir)

class AbstractScanElement(ABC):

    scan_dir= ''

    def __init__(self,dir):
        self.dir = dir
        self.init_dir()
        self.create_json_config()

    @abstractmethod
    def scan(self):
        pass

    def create_json_config(self):
        if Path(self.dir + '\\config.json').is_file() is False:
            f = open(self.dir + '\\config.json', "x")
            f.write('{}')
            f.close()

    def init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir + '\\' + dir) is False:
                os.makedirs(self.dir + '\\' + dir)


class ScanSerie(AbstractScanElement):

    scan_dir = 'movies'
    base_dir=['movies','photos\\DATA','banners','stars']

    def scan(self):
        dir_list = os.listdir(self.dir + '\\' + self.scan_dir);
        for dir in dir_list:
            is_dir = os.path.isdir(self.dir + '\\' + self.scan_dir + '\\' + dir)
            if is_dir:
                dir_list_el = os.listdir(self.dir + '\\' + self.scan_dir + '\\' + dir+'\\DATA')
                for el_in_dir in dir_list_el:
                    print(el_in_dir)

class ScanStar(AbstractScanElement):

    def scan(self):
        pass

class ScanProducent(AbstractScanElement):

    def scan(self):
        dir_list = os.listdir(self.dir+'\\'+self.scan_dir);
        for dir in dir_list:
            print(dir)

class StarsDir(AbstractScan):
    FactoryScan = ScanStar

class SeriesDir(AbstractScan):
    FactoryScan = ScanSerie

class ProducentsDir(AbstractScan):
    FactoryScan = ScanProducent




