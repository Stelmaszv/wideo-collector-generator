import os
from abc import ABC, abstractmethod

class ScanDirs:

    def __init__(self,dir):
        self.dir = dir

    def start(self):
        scan_dir= {
            "stars"  :ScanStars,
            "series" :ScanSeries,
            "producents": ScanProducents,
        }
        for dir in self.dir:
            if dir != "movies":
                print('Scaning Dir ... Dir '+dir+'')
                dir=scan_dir[dir](self.dir[dir])
                dir.init_dir()
                dir.scan()


class AbstractScan(ABC):
    base_dir=['A-D','E-H','I-L','M-P','R-U','W-Z']
    def __init__(self,dir):
        self.dir=dir

    @abstractmethod
    def scan(self):
        pass

    @abstractmethod
    def init_dir(self):
        pass

    def base_init_dir(self):
        for dir in self.base_dir:
            if os.path.isdir(self.dir+'\\'+dir) is False:
                os.mkdir(self.dir+'\\'+dir)

class ScanStars(AbstractScan):

    def scan(self):
        pass

    def init_dir(self):
        self.base_init_dir()

class ScanSeries(AbstractScan):

    def scan(self):
        pass

    def init_dir(self):
        self.base_init_dir()

class ScanProducents(AbstractScan):

    def scan(self):
        pass

    def init_dir(self):
        self.base_init_dir()
