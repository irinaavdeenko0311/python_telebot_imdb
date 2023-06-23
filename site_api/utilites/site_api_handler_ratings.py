""" Модуль для обработки информации о рейтингах фильмов """

from typing import List, Tuple
import re
import requests
from requests import Response
import random

from site_api.utilites.site_api_pattern import ApiCommon, ApiTop


class Top100(ApiTop):
    """ Класс для работы с полученной информацией 'Топ 100' фильмов. """

    def get_top_100(self) -> List[Tuple]:
        """ Метод для формирования списка, содержащего строку из id фильма и названия """
        return [(i["imdbid"], i["title"]) for i in self.get_response().json()]


class GenresList(ApiCommon):
    """ Класс для работы с полученной информацией о жанрах фильмов. """

    def __init__(self):
        super().__init__()
        self.url += "title/list-popular-genres"

    def get_response(self) -> Response:
        """ Переопределение метода базового класса - отсутствует params. """
        return requests.get(self.url, headers=self._headers)

    def get_genres(self) -> List:
        """ Метод для формирования списка жанров. """
        return [i['description'] for i in self.get_response().json()['genres']]


class MoviesByGenre(ApiCommon):
    """ Класс для работы с полученной информацией о фильмах, лучших в жанре. """

    def __init__(self, genre: str):
        super().__init__()
        self.url += "title/v2/get-popular-movies-by-genre"
        self.querystring = {"genre": genre, "limit": "30"}

    def get_movies_by_genre(self) -> List:
        """ Метод для формирования списка фильмов, лучших в жанре. Содержит только id. """
        return [re.search(r'\btt\d+', i).group(0) for i in self.get_response().json()]


class MovieName(ApiCommon):
    """ Класс для работы с базовой информацией о фильме. Необходимо получить только название. """

    def __init__(self, movie_id: str):
        super().__init__()
        self.url += "title/get-base"
        self.querystring = {"tconst": movie_id}

    def get_movie_name(self) -> str:
        """ Метод, вычленяющий только название фильма """
        return self.get_response().json()['title']


class PopularMoviesToday(ApiCommon):
    """ Класс для работы с информацией о фильмах, популярных сегодня. """

    def __init__(self):
        super().__init__()
        self.url += "title/get-most-popular-movies"
        self.querystring = {"currentCountry":"US", "purchaseCountry":"US", "homeCountry":"US"}

    def get_popular_movies(self) -> List:
        """ Метод, вычленяющий id фильмов, формирует список из 10-ти фильмов. """
        response = self.get_response().json()
        return [re.search(r'\btt\d+', response[i]).group(0) for i in range(10)]

    def get_random_movie(self):
        """ Метод для получения случайного фильма из списка. """
        return random.choice(self.get_popular_movies())


if __name__ == '__main__':
    Top100()
    GenresList()
    MoviesByGenre()
    MovieName()
    PopularMoviesToday()
