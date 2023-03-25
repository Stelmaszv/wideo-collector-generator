from scrabers.FilmWEB import FilmWEB
from scrabers.IMDB import IMDB
from scrabers.BB import BB
from scrabers.THC import THC

scrapers={
    "film_web"    :FilmWEB,
    "imdb"        :IMDB,
    "bb"          :BB,
    'THC'         :THC
}

defult_stars_scraper = IMDB.StarsScraper