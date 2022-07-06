import os
import json
from os.path import exists
from core.settings import error_type
from pathlib import Path

class ValidJson:

    def __init__(self,data_JSON):
        self.data=data_JSON
        self.dirs_data={}

    def valid_index(self):
        try:
            self.data['dirs']
        except KeyError:
            if error_type:
                raise KeyError('Validate data.JSON file ... Dirs index not exist !')
            else:
                exit('Validate data.JSON file ... Dirs index not exist !')

    def check_dirs(self):

        def valid_el_index(var,index):
            if var is not True:
                if error_type:
                    raise KeyError('Validate data.JSON file ... missing index  '+index+' !')
                else:
                    exit('Validate data.JSON file ... missing index  ' + index + ' !')

        def find_var(var):
            for dir in self.data['dirs']:
                try:
                    dir['type']
                except KeyError:
                    if error_type:
                        raise KeyError('Validate data.JSON file ... missing index type fir ' + str(var) + ' !')
                    else:
                        exit('Validate data.JSON file ... missing index type fir ' + str(var) + ' !')
                else:
                    if dir['type'] == var:
                        return True
            return False

        def valid_dirs_url():
            for dir in self.data['dirs']:
                try:
                    dir['dir']
                except KeyError:
                    if error_type:
                        raise KeyError('Validate data.JSON file ... missing index dir ' + str(dir) + ' !')
                    else:
                        exit('Validate data.JSON file ... missing index dir ' + str(dir) + ' !')
                else:
                    dir_error = os.path.isdir(dir['dir'])
                    if dir_error is False:
                        if error_type:
                            raise IsADirectoryError('Validate data.JSON file ... Dir for ' + dir['type'] + ' is Invilid or is Crypted !')
                        else:
                            exit('Validate data.JSON file ... Dir for ' + dir['type'] + ' is Invilid or is Crypted !')
                    else:
                        self.dirs_data[dir['type']] = dir['dir'] + '\\' + dir['type']
                        if os.path.isdir(dir['dir']+'\\'+dir['type']) is False:
                            os.mkdir(dir['dir']+'\\'+dir['type'])

        valid_el_index(find_var('stars'),'stars')
        valid_el_index(find_var('series'), 'series')
        valid_el_index(find_var('producents'), 'producents')
        valid_el_index(find_var('movies'), 'movies')
        valid_dirs_url()

    def set_dirs(self,dir):
        return self.dirs_data

    def valid(self):
        self.valid_index()
        self.check_dirs()
        print('Validate data.JSON file ... OK')

class LoopRun:
    moduls = []

    def __init__(self,moduls):
        self.moduls=moduls

    def run_object(self, Obj, method, run, start_string, end_string):
        if run:
            print(start_string)
            method = getattr(Obj, method)
            method()
            print(end_string)

    def loop(self):
        for object in self.moduls:
            self.run_object(object['obj'], object['method'], object['stan'], object['start_mes'], object['end_mees'])

class CreateDist():
    shema_url = 'json_schema\\dist.JSON'
    def __init__(self):
        if exists('dist.json') is False:
            f = open('dist.json', "x")
            #f.write("{'series': {} , 'movies':{}}")
            f.write(Path(self.shema_url).read_text())
            f.close()



