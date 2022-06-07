from scrabers.scrapers import scrapers,defult_stars_scraper as defult_stars_scraper_var
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
default_scraper_var='imdb'
scraper=scrapers[default_scraper_var] #film_web
download_galery=True
defult_stars_scraper=defult_stars_scraper_var