error_type = False  #True for full mess
setings_array = {
    "scan_dir": True,
    "scraper" : True,
    "config"  : True
}
movie_ext= ('.avi','.mkv','.mp4','.wmv')
#stars
ethnicity=('Asian','Euro','Arab')
hair_color=('Blond','Brown')
#scraper
from core.scraper import  FilmWEBUrl,FilmWEBUrlList,FilmWEBUrlListSearch
srapers={
    "film_web_url"    :FilmWEBUrl,
    "film_web_list"   :FilmWEBUrlList,
    "film_web_search" :FilmWEBUrlListSearch,
}
defult_sraper=True
sraper=srapers['film_web_url'] #film_web