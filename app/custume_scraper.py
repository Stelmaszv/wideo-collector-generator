from core.scraper import AbstractScraperMovies


class FilmWEBMovies(AbstractScraperMovies):
    def set_show_name(self)->str:
        return ''

    def description(self)->str:
        return  ''

    def date_relesed(self)->str:
        return  ''

    def cover(self)->str:
        return  ''

    def country(self)->str:
        return  ''

    def poster(self)->str:
        return  ''

class FilmWEB:
    MoviesScraber = FilmWEBMovies