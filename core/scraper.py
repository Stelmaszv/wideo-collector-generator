import json
import os
from abc import ABC,abstractmethod

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import validators

from core.helper import DataValid

chrome = webdriver.Chrome(ChromeDriverManager().install())
class AbstractScraperMovies(ABC):

    url=''
    debug=False
    cover=False

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

    def check_dist_format(self,data,index):
        for el in data:
            if index not in data[el]:
                raise TypeError('invalid_format')

    def add_stars(self,nstars,stars):
        from core.dir import StarElment
        stars_dist={}
        for star in nstars:
            stars_dist[star]={"star_name":star}
            StarElment(star).add()
        stars_dist.update(stars)
        return stars_dist

    def add_tags(self,add_tag,tags):
        def valid_tags(tags):
            valid_tags_return=[]
            for tag in tags:
                tag = tag.capitalize()
                valid_tags_return.append(tag)
            return valid_tags_return
        tags_valid=valid_tags(add_tag)
        tag_dist = {}
        for tag in tags_valid:
            tag_dist[tag] = {"tag_name": tag}
        tags.update(tag_dist)
        return {}

    def get_stars_dict(self,stars):
        return self.add_stars(self.set_stars(), stars)

    def get_tags_dict(self,tags):
        return self.add_tags(self.set_tag(), tags)

    def from_dist_to_list(self,dist):
        list=[]
        for el in dist:
            list.append(el)
        return list

    def get_tags_list(self,tags):
        tags_array = self.from_dist_to_list(tags)
        tags_array.extend(self.set_tag())
        return tags_array

    def get_stars_list(self,stars):
        stars_array = self.from_dist_to_list(stars)
        stars_array.extend(self.set_tag())
        return stars_array

    def get_show_name(self):
        return self.check_type('str',self.set_show_name())

    def get_description(self):
        return self.check_type('str',self.set_description())

    def get_cover(self,cover):
        if self.cover:
            return self.check_type('str', self.set_cover())
        return cover

    def get_country(self):
        return self.check_type('str', self.set_country())

    def get_poster(self):
        return self.check_type('str', self.set_poster())

    def get_date_relesed(self,elment):
        data =self.set_date_relesed()
        DV=DataValid()
        DV.set_data(data,False,elment,self.index)
        if(DV.is_valid()):
            return data

    @abstractmethod
    def set_stars(self):
        pass

    @abstractmethod
    def set_tag(self):
        pass

    @abstractmethod
    def set_show_name(self):
        pass

    @abstractmethod
    def set_description(self):
        pass

    def set_date_relesed(self):
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
