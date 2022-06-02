import os
from abc import ABC,abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
chrome = webdriver.Chrome(ChromeDriverManager().install())

class AbstractScraperMovies(ABC):

    url=''

    def __init__(self,dir):
        self.chrome=chrome
        if self.url:
            self.chrome.get(self.url)

    @abstractmethod
    def set_show_name(self)->str:
        pass

    @abstractmethod
    def description(self)->str:
        pass

    @abstractmethod
    def date_relesed(self)->str:
        pass

    @abstractmethod
    def cover(self)->str:
        pass

    @abstractmethod
    def country(self)->str:
        pass

    @abstractmethod
    def poster(self)->str:
        pass

class AbstractScraperSeriesList(ABC):

    def __init__(self, dir):
        self.list_error = os.path.exists(dir['dir']+'/scraber_list.json')
        if self.list_error is False:
            print('Miss List for '+dir['name']+'!')

    @abstractmethod
    def set_show_name(self)->str:
        pass

    @abstractmethod
    def description(self)->str:
        pass

    @abstractmethod
    def date_relesed(self)->str:
        pass

    @abstractmethod
    def cover(self)->str:
        pass

    @abstractmethod
    def country(self)->str:
        pass

    @abstractmethod
    def poster(self)->str:
        pass