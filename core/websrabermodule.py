import ast
import json
import os
from abc import ABC,abstractmethod
from core.settings import default_scraper, scrapers, scraper,download_galery

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

    Scraper =None

    def set_data(self, index, element):
        self.index = index
        self.element = element

    def scraper(self,index,element):
        self.set_data(index,element)
        self.on_scraper()

    @abstractmethod
    def on_scraper(self):
        pass

    def start_scraping(self,data)->data:
        return data

    def start_scraping_main(self,data):
        data = self.start_scraping(data)
        for el in data:
            db[self.index][self.element][el] = data[el]
        os.remove("dist.json")
        a_file = open("dist.json", "w")
        json.dump(db, a_file)
        a_file.close()

class MoviesScraperFactory(AbstractScraperFactory):

    def on_scraper(self):
        with open(db[self.index][self.element]['dir'] + '/config.JSON') as f:
            data = json.load(f)
            series_name = db[self.index][self.element]['series']
            series_index = db['series'][series_name]

            self.Scraper = None

            if "scraper" in data:
                self.Scraper = scrapers[data['scraper']]()
            else:
                if "scraper" in  series_index:
                    self.Scraper = scrapers[series_index["scraper"]]()
                else:
                    if default_scraper is True:
                        self.Scraper = scraper()
            if self.Scraper:
                self.MoviesScraper = self.Scraper.MoviesScraper
                type = self.MoviesScraper.type
                if type == 'list':
                    series_name = db[self.index][self.element]['series']
                    series_index = db['series'][series_name]
                    series_scraper = self.Scraper.SeriesScraper(series_index)
                    if series_scraper.list_error:
                        url = series_scraper.faind(db[self.index][self.element]['name'])
                        self.MoviesScraper = self.MoviesScraper(url, db[self.index][self.element])

        if self.Scraper:
            self.start_scraping_main(data)
            os.remove(db[self.index][self.element]['dir'] + '\config.JSON')
            a_file = open(db[self.index][self.element]['dir'] + "\config.JSON", "x")
            json.dump(data, a_file)
            a_file.close()

    def start_scraping(self,data)->data:
        data['show_name']    = self.MoviesScraper.get_show_name()
        data['description']  = self.MoviesScraper.get_description()
        data['date_relesed'] = self.MoviesScraper.get_date_relesed(db[self.index][self.element])
        data['country']      = self.MoviesScraper.get_country()
        data['poster']       = self.MoviesScraper.get_poster()
        data['cover']        = self.MoviesScraper.get_cover(data['cover'])
        self.MoviesScraper.get_stars(db[self.index][self.element]['stars'])
        #data['tags']        = self.MoviesScraper.get_tags(data['tags'])
        if download_galery:
            self.MoviesScraper.galery()
        return data

class SeriesScraperFactory(AbstractScraperFactory):

    def on_scraper(self):
        with open(db[self.index][self.element]['dir'] + '/config.JSON') as f:
            data = json.load(f)
            if "scraper" in data:
                self.Scraper = scrapers[data['scraper']]().SeriesScraper(db[self.index][self.element])
            else:
                self.Scraper = scraper().SeriesScraper(db[self.index][self.element])
            type = self.Scraper.type
            if type == 'list':
                if self.Scraper.list_error:
                    self.start_scraping_main(data)

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

