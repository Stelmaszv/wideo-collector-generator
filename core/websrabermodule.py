import ast
from abc import ABC

with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)

class WebScraperModule:

    def start(self):
        dirs= {
            "movies" : MoviesScraper,
            "stars"  : StarsScraper,
            "series" : SeriesScraper
        }
        for dir in db:
            if dir != "tags" and dir != 'producents':
                Scraper=dirs[dir]()
                Scraper.set_dir(dir)
                Scraper.start_scraper()


class AbstractScraper(ABC):

    def set_dir(self,dir):
        self.dir=dir

class MoviesScraper(AbstractScraper):

    def start_scraper(self):
        print('movies scrabing')

class StarsScraper(AbstractScraper):

    def start_scraper(self):
        print('stars scrabing')

class SeriesScraper(AbstractScraper):

    def start_scraper(self):
        print('Series scrabing')