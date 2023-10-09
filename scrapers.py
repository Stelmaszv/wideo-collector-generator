from scrabers.FilmWEB import FilmWEB
from scrabers.IMDB import IMDB
from scrabers.BB import BB
from scrabers.rj import RJ
from scrabers.THC import THC
from scrabers.Downloader import Downloader

scrapers={
    "film_web"    :FilmWEB,
    "imdb"        :IMDB,
    "bb"          :BB,
    "RJ"          :RJ,
    'THC'         :THC,
    'Downloader'  :Downloader
}

defult_stars_scraper = IMDB.StarsScraper