from scrabers.scrapers import scrapers
error_type = False  #True for full mess
settings_array = {
    "scan_dir": True,
    "scraper" : True,
    "config"  : True
}
movie_ext= ('.avi','.mkv','.mp4','.wmv')
#stars
ethnicity=('Asian','Euro','Arab')
hair_color=('Blond','Brown')
#scraper
default_scraper=True
scraper=scrapers['film_web'] #film_web