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

    def check_type(self,var,method):
        method_var=method
        type_var = type(method_var).__name__
        if method_var!=None:
            if type_var == var:
                return  method_var
            else:
                raise TypeError('Invalid return value for field requrid '+var+' == '+type_var)
        raise TypeError('Invalid return value for field requrid ' + var + ' == NONE')

    def get_show_name(self):
        return self.check_type('str',self.set_show_name())

    def get_description(self):
        return self.check_type('str',self.set_description())

    def get_cover(self,cover):
        if cover:
            return self.check_type('str',self.set_cover())
        return ''

    def get_country(self):
        return self.check_type('str', self.set_country())

    def get_poster(self):
        return self.check_type('str', self.set_poster())

    @abstractmethod
    def set_show_name(self):
        pass

    @abstractmethod
    def set_description(self):
        pass

    def date_relesed(self):
        return  'YEAR-MOUNT-DAY'

    @abstractmethod
    def set_cover(self):
        pass

    @abstractmethod
    def set_country(self):
        pass

    @abstractmethod
    def set_poster(self):
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
