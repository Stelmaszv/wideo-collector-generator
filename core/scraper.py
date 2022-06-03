import json
import os
from abc import ABC,abstractmethod

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import validators
chrome = webdriver.Chrome(ChromeDriverManager().install())
class AbstractScraperMovies(ABC):

    url=''
    debug=False
    def __init__(self,url,index):
        self.index=index
        self.url = url
        self.chrome=chrome
        if validators.url(self.url):
            print('Scraping Movie ... ' + self.index['name'])
            self.chrome.get(self.url)
        if self.debug:
            print(self.url)

    def save_in_galery(self,photos):
        for el in photos:
            name = el.split('/')[len(el.split('/')) - 1]
            img_data = requests.get(el).content
            with open(self.index['dir']+'/' + name, 'wb') as handler:
                print('Downloading galery for '+self.index['name']+'  from ' + el)
                handler.write(img_data)


    @abstractmethod
    def set_show_name(self)->str:
        pass

    @abstractmethod
    def description(self)->str:
        pass

    def date_relesed(self)->str:
        return  'YEAR-MOUNT-DAY'

    @abstractmethod
    def cover(self)->str:
        pass

    @abstractmethod
    def country(self)->str:
        pass

    @abstractmethod
    def poster(self)->str:
        pass

    def galery(self):
        pass

class AbstractScraperMoviesList(AbstractScraperMovies):
    type = 'list'

class AbstractScraperSeriesList(ABC):

    def __init__(self, index):
        self.index=index
        self.list_location=self.index['dir']+'/scraber_list.json'
        self.list_error = os.path.exists(self.list_location)
        self.list_error_mess()

    def faind(self,name):
        self.list_error_mess()
        with open(self.list_location) as f:
            data = json.load(f)
            return data[name]

    def list_error_mess(self):
        if self.list_error is False:
            print('Miss List for ' +self.index['name']+ '!')
            return
