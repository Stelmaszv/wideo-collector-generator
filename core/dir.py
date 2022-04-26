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
                scan_dir[dir](self.dir[dir]).scan()

class AbstractScan(ABC):

    def __init__(self,dir):
        self.dir=dir

    @abstractmethod
    def scan(self):
        pass

class ScanStars(AbstractScan):

    def scan(self):
        pass

class ScanSeries(AbstractScan):

    def scan(self):
        pass

class ScanProducents(AbstractScan):

    def scan(self):
        pass