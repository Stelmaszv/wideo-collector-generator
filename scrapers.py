from scrabers.custume_scraper import FilmWEB
from scrabers.IMDB import IMDB

scrapers={
    "film_web"    :FilmWEB,
    "imdb"        :IMDB,
}
defult_stars_scraper = IMDB.StarsScraper