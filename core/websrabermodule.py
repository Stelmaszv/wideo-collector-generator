import ast
with open('dist.json') as f:
    data = f.read()
    db = ast.literal_eval(data)


class WebSraberModule:

    def __int__(self):
        print('init')

    def start(self):
        config_dirs= {
            "movies" :MoviesScraber,
            "stars": StarsScraber,
            "series": SeriesScraber,
        }
        for dir in db:
            if dir != "tags" and dir != 'producents':
                config_dirs[dir]().start_config()

class MoviesScraber:

    def start_config(self):
        print('movies scrabing')


class StarsScraber:

    def start_config(self):
        print('stars scrabing')

class SeriesScraber:


    def start_config(self):
        print('Series scrabing')