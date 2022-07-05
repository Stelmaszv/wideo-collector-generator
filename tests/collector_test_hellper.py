import json
import os
import shutil
from pathlib import Path

class CollectorInnit:

    collector_dirs=['producents','series','stars','movies']

    def init_dirs(self):
        for dir in self.collector_dirs:
            os.makedirs('test_env/'+dir)

    def delete_collector_dir(self):
        shutil.rmtree('test_env',ignore_errors=True)

    def add_movie_dir(self,dir):
        os.makedirs('test_env\\movies\\' + dir)
        return 'test_env\\movies\\' + dir

    def add_star_dir(self,dir):
        os.makedirs('test_env\\stars\\' + dir)
        return 'test_env\\stars\\' + dir

    def add_config(self,dir):
        f = open(dir + '\\config.json', "x")
        f.write(json.dumps('{}'))
        f.close()

class CollectorEnvConfig:

    def data_config(self):
        f = open('data.json', "x")
        f.write(Path('data_test_shema.JSON').read_text())
        f.close()

    def dist_create(self):
        f = open('dist.json', "x")
        f.write(json.dumps('{}'))
        f.close()

    def remove_config(self):
        os.remove('data.json')

    def remove_dist(self):
        os.remove('dist.json')



