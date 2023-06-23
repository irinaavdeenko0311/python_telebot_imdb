""" Модуль для обработки информации об актерах """

from typing import Dict, Tuple
import re
import random

from site_api.utilites.site_api_pattern import ApiCommon


class ActorsByName(ApiCommon):
    """ Класс для работы с полученной информацией об актерах по заданному имени. """

    def get_actors_with_id(self, name) -> Dict:
        """ Метод, вычленяющий из полученной информации словарь с id и именами актеров. """
        return super().get_common_info(name=name, id_startswith='nm')


class ActorInfo(ApiCommon):
    """ Класс для работы с полученной информацией об актере по id. """

    def __init__(self, actor_id: str):
        super().__init__()
        self.url += "actors/get-bio"
        self.querystring = {"nconst": actor_id}

    def get_info_about_actor(self) -> Tuple:
        """ Метод, вычленяющий нужную информацию об актере,
        фото и размер фото (с целью проверки превышения допустимого размера). """
        response = self.get_response().json()
        info = dict()
        for i in ['name', 'birthDate', 'realName', 'trademarks']:
            try:
                if i == 'trademarks':
                    info['Random fact'] = random.choice(response[i])
                else:
                    info[i.title()] = response[i]
            except KeyError:
                info[i] = '-'
        info = [f'{k}: {v}' for k, v in info.items()]
        try:
            image_url = response['image']['url']
            image_size = response['image']['height'] + response['image']['width']
        except KeyError:
            image_url = "https://www.meiji.ac.jp/cip/english/wr-common/images/img_noimage.gif"
            image_size = 0
        return '\n'.join(info), image_url, image_size


class ActorMovies(ApiCommon):
    """ Класс для работы с полученной информацией о главных фильмах, в которых актер играл. """

    def __init__(self, actor_id: str):
        super().__init__()
        self.url += "actors/get-known-for"
        self.querystring = {"nconst": actor_id}

    def get_actor_movies_with_id(self) -> Dict:
        """ Метод, вычленяющий id фильмов и их названия. """
        info = dict()
        for i in self.get_response().json():
            key = re.search(r'\btt\d+', i['title']['id']).group(0)
            value = i['title']['title']
            info[key] = value
        return info


class NewMoviesOfActor(ApiCommon):
    """ Класс для работы с полученной информацией о всей фильмографии актера. """
    def __init__(self, actor_id: str):
        super().__init__()
        self.url += "actors/get-all-filmography"
        self.querystring = {"nconst": actor_id}

    def get_new_movies(self):
        movies = dict()
        for i in self.get_response().json()['filmography']:
            if i['status'] == 'released' and 'attr' not in i:
                key = re.search(r'\btt\d+', i['id']).group(0)
                value = i['title']
                movies[key] = value
            if len(movies) == 4:
                break
        return movies


if __name__ == '__main__':
    ActorsByName()
    ActorInfo()
    ActorMovies()
    NewMoviesOfActor()
