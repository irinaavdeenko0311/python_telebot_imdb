""" Модуль для обработки информации о фильмах """

from typing import Dict, Tuple
import re

from site_api.utilites.site_api_pattern import ApiCommon
from site_api.utilites.site_api_handler_ratings import MovieName


class MovieByTitle(ApiCommon):
    """ Класс для работы с полученной информацией о фильмах по заданному названию. """

    def get_movies_with_id(self, name) -> Dict:
        """ Метод, вычленяющий из полученной информации словарь с id фильмов и названиями. """
        return super().get_common_info(name=name, id_startswith='tt')


class MovieInfo(ApiCommon):
    """ Класс для работы с полученной информацией о фильме по id. """

    def __init__(self, movie_id: str):
        super().__init__()
        self.url += "title/get-overview-details"
        self.querystring = {"tconst": movie_id,"currentCountry": "US"}

    def get_info_about_movie(self) -> Tuple:
        """ Метод, вычленяющий нужную информацию о фильме,
        фото и размер фото (с целью проверки превышения допустимого размера). """
        response = self.get_response().json()
        info = list()

        first_str = list()
        for i in ['title', 'titleType', 'year']:
            try:
                first_str.append(str(response['title'][i]))
            except KeyError:
                first_str.append(' ')
        info.append(', '.join(first_str))

        second_str = list()
        try:
            rating = f"Rating: {response['ratings']['rating']}"
            second_str.append(rating)

            genres = f"Genres: {', '.join(response['genres'])}"
            second_str.append(genres)

            info.append(', '.join(second_str))
            info.append(response['plotOutline']['text'])
        except KeyError:
            pass

        try:
            image_url = response['title']['image']['url']
            image_size = response['title']['image']['height'] + response['title']['image']['width']
        except KeyError:
            image_url = "https://www.meiji.ac.jp/cip/english/wr-common/images/img_noimage.gif"
            image_size = 0

        return '\n'.join(info), image_url, image_size


class MovieActors(ApiCommon):
    """ Класс для работы с информацией об актерах, играющих главные роли в фильме. """

    def __init__(self, movie_id: str):
        super().__init__()
        self.url += "title/find"
        self.querystring = {"q": movie_id}

    def get_movie_actors_with_id(self) -> Dict:
        """ Метод, вычленяющий id актеров и их имена. """
        info = dict()
        for i in self.get_response().json()['results'][0]['principals']:
            key = re.search(r'\bnm\d+', i['id']).group(0)
            value = i['name']
            info[key] = value
        return info


class LooksLikeMovie(ApiCommon):
    """ Класс для работы с информацией о фильмах, похожих на другой фильм. """
    def __init__(self, movie_id: str):
        super().__init__()
        self.url += "title/get-more-like-this"
        self.querystring = {"tconst": movie_id, "currentCountry":"US", "purchaseCountry":"US"}

    def get_movies_looks_like(self) -> Dict:
        response = self.get_response().json()
        movies_looks_like = dict()
        for i in range(5):
            key = re.search(r'\btt\d+', response[i]).group(0)
            value = MovieName(key).get_movie_name()
            movies_looks_like[key] = value
        return movies_looks_like


if __name__ == '__main__':
    MovieByTitle()
    MovieInfo()
    MovieActors()
    LooksLikeMovie()
