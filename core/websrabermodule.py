import ast
import json
from abc import ABC,abstractmethod

with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class WebScraperModule:

    def start(self):
        dirs= {
            "movies" : MoviesScraperDir,
            "series" : SeriesScraperDir,
            "stars"  : StarsScraperDir
        }
        for dir in db:
            if dir != "tags" and dir != 'producents' and dir != 'stars':
                Scraper=dirs[dir](dir)
                Scraper.start_scraper()

class AbstractScraperFactory(ABC):

    def set_data(self, index, element):
        self.index = index
        self.element = element

    def scraper(self,index,element):
        self.set_data(index,element)
        self.on_scraper()

    @abstractmethod
    def on_scraper(self):
        pass

class MoviesScraperFactory(AbstractScraperFactory):

    def on_scraper(self):
        with open(db[self.index][self.element]['dir'] + '/config.JSON') as f:
            data = json.load(f)
            print(data['show_name'])

class SeriesScraperFactory(AbstractScraperFactory):

    def on_scraper(self):
        print('Series')

class StartScraperFactory(AbstractScraperFactory):

    def on_scraper(self):
        print('Stars')

class AbstractDirScraper(ABC):

    scraper_mess=''
    FactoryScraper=None

    def __init__(self,index):
        self.index=index

    def start_scraper(self):
        print(self.scraper_mess)
        for el in db[self.index]:
            self.FactoryScraper().scraper(self.index,el)

class MoviesScraperDir(AbstractDirScraper):
    FactoryScraper = MoviesScraperFactory
    scraper_mess = 'Scraping Movies ... Start'

class SeriesScraperDir(AbstractDirScraper):
    FactoryScraper = SeriesScraperFactory
    scraper_mess = 'Scraping Series ... Start'

class StarsScraperDir(AbstractDirScraper):
    FactoryScraper = StartScraperFactory
    scraper_mess = 'Scraping Start ... Start'

