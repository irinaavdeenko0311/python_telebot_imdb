""" Основной модуль для работы с БД """

from typing import Tuple

from database.utilites.combined import DbWithCombinedMethods
from site_api.core import common_api


class DbImdb(DbWithCombinedMethods):
    """ Класс 'БД для работы с сайтом imdb' """

    """ Таблица 'users': """
    def check_presence_and_create_table_users_id(self) -> None:
        """ Метод для проверки наличия таблицы с id пользователей в БД. Если её нет - таблица создается. """
        self.check_presence_and_create_table(table_name='users', columns={'users_id': 'TEXT'})

    """ Таблица пользователя: """
    def check_presence_and_create_table_user_requests(self, user_id: int) -> None:
        """ Метод для проверки наличия таблицы пользователя в БД.
        Если её нет - таблица создается и пользователь добавляется в таблицу 'users'."""
        self.check_presence_and_create_table(table_name=user_id, columns={'requests': 'TEXT'})
        self.check_presence_and_insert_value(value=user_id, column_name='users_id', table_name='users')

    def check_presence_and_insert_value_to_requests(self, user_id: int, value: str) -> None:
        """ Метод для проверки наличия запроса пользователя в его таблице. Если его нет - это значение добавляется. """
        self.check_presence_and_insert_value(value=value, table_name=user_id, column_name='requests')

    """ Таблица со всеми запросами пользователей 'all_data': """
    def check_presence_and_create_table_all_data(self) -> None:
        """ Метод для проверки наличия таблицы со всеми запросами пользователей (актеры и фильмы) в БД.
        Если её нет - таблица создается. """
        self.check_presence_and_create_table(table_name='all_data', columns={'id': 'TEXT', 'name': 'TEXT'})

    def check_presence_and_insert_value_to_all_data(self, value: Tuple) -> None:
        """ Метод для проверки наличия запроса в таблице. Если его нет - это значение добавляется. """
        self.check_presence_and_insert_value(value=value, table_name='all_data', column_name='id')

    def get_name(self, name_id: str) -> str:
        """ Метод для получения из базы имени актера/названия фильма по id. """
        name = self.get_cell_value(table_name='all_data', find_column='name', column='id', value=name_id)
        return name[0][0]

    """ Таблица 'top_100' фильмов: """
    def check_presence_create_and_insert_table_top_100(self) -> None:
        """ Метод для проверки наличия таблицы 'top_100' в БД. Если её нет - таблица создается и заполняется. """
        self.check_presence_create_and_insert_table(table_name='top_100', columns={'id': 'TEXT', 'name': 'TEXT'},
                                                    insert_method=self.insert_top_100)

    def insert_top_100(self) -> None:
        """ Метод для заполнения таблицы Топ 100. """
        top = common_api.Top100().get()
        for i in top:
            self.insert_to_table(table_name='top_100', value=(i[0], i[1]))
            self.check_presence_and_insert_value_to_all_data((i[0], i[1]))

    """ Таблица с жанрами: """
    def check_presence_create_and_insert_table_movie_genres(self) -> None:
        """ Метод для проверки наличия таблицы жанров в БД. Если её нет - таблица создается и заполняется. """
        self.check_presence_create_and_insert_table(table_name='movie_genres', columns={'genres': 'TEXT'},
                                                    insert_method=self.insert_movie_genres)

    def insert_movie_genres(self) -> None:
        """ Метод для заполнения таблицы с жанрами. """
        genres = common_api.GenresList().get()
        for i in genres:
            self.insert_to_table(table_name='movie_genres', value=i)

    """ Таблица с фильмами жанра: """
    def check_presence_create_and_insert_table_movies_by_genre(self, genre) -> None:
        """ Метод для проверки наличия таблицы с фильмами определенного жанра в БД.
         Если её нет - таблица создается и заполняется. """
        self.check_presence_create_and_insert_table(table_name=genre, columns={'movie_id': 'TEXT'},
                                                    insert_method=self.insert_movie_by_table_genre, genre_flag=genre)

    def insert_movie_by_table_genre(self, genre) -> None:
        """ Метод для заполнения таблицы с фильмами определенного жанра. """
        movie_id_by_genre = common_api.MoviesByGenre(genre).get()
        for i in movie_id_by_genre:
            self.insert_to_table(table_name=genre, value=i)


name_db = 'history.db'

db = DbImdb(name_db)

if __name__ == '__main__':
    DbImdb()
