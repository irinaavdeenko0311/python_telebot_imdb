""" Модуль, содержащий шаблоны API """

import requests
from requests import Response

from settings import SiteSettings

site = SiteSettings()


class ApiCommon:
    """ Класс для работы с API 'Online Movie Database'. """

    def __init__(self):
        self.url = "https://online-movie-database.p.rapidapi.com/"
        self.querystring = {"q": ""}
        self._headers = {
            "X-RapidAPI-Key": site.api_key.get_secret_value(),
            "X-RapidAPI-Host": site.api_host_common
        }

    def get_common_info(self, name, id_startswith):
        self.url += "auto-complete"
        self.querystring = {"q": name}

        name_with_id = dict()
        for i in self.get_response().json()['d']:
            if i['id'].startswith(id_startswith):
                key = i['id']
                value = i['l']
                name_with_id[key] = value
            if len(name_with_id) == 4:
                break
        return name_with_id

    def get_response(self) -> Response:
        return requests.get(self.url, headers=self._headers, params=self.querystring)


class ApiTop:
    """ Класс для работы с API 'IMDb Top 100 Movies'. """

    def __init__(self):
        self.url = "https://imdb-top-100-movies.p.rapidapi.com/"
        self._headers = {
            "X-RapidAPI-Key": site.api_key.get_secret_value(),
            "X-RapidAPI-Host": site.api_host_top
        }

    def get_response(self) -> Response:
        return requests.get(self.url, headers=self._headers)


if __name__ == '__main__':
    ApiCommon()
    ApiTop()
