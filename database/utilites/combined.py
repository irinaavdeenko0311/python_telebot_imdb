""" Модуль, содержащий модель БД с дополнительными методами (проверка наличия и создание одновременно) """

from typing import Any, Dict, Callable

from database.utilites.model import ModelDb


class DbWithCombinedMethods(ModelDb):
    """ Класс 'Модель БД с дополнительными методами'. """

    def check_presence_and_create_table(self, table_name: Any, columns: Dict) -> None:
        """ Метод для проверки наличия таблицы в БД. Если её нет - таблица создается. """
        if not self.check_presence_table(table_name):
            self.create_table(table_name=table_name, columns=columns)

    def check_presence_create_and_insert_table(self, table_name: Any, columns: Dict,
                                               insert_method: Callable, genre_flag=None) -> None:
        """ Метод для проверки наличия таблицы в БД. Если её нет - таблица создается и заполняется. """
        if not self.check_presence_table(table_name):
            self.create_table(table_name=table_name, columns=columns)
            if genre_flag:
                insert_method(genre_flag)
            else:
                insert_method()

    def check_presence_and_insert_value(self, value: Any, column_name: str, table_name: Any) -> None:
        """ Метод для проверки наличия значения в таблице. Если его нет - это значение добавляется. """
        if not self.check_presence(table_name=table_name, column_name=column_name, value=value):
            self.insert_to_table(table_name=table_name, value=value)


if __name__ == '__main__':
    DbWithCombinedMethods()
