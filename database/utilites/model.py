""" Модуль, содержащий модель базы данных """

import sqlite3
from typing import Any, List, Dict, Tuple


class ModelDb:
    """ Класс 'Модель базы данных'. """

    def __init__(self, db_name: str) -> None:
        self._connect = sqlite3.connect(db_name, check_same_thread=False)
        self._cursor = self._connect.cursor()

    def create_table(self, table_name: Any, columns: Dict) -> None:
        """ Метод для создания таблицы. """
        if isinstance(table_name, int):
            table_name = f"'{table_name}'"
        columns = ', '.join([f'{key} {value}' for key, value in columns.items()])
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({columns})")
        self.commit()

    def insert_to_table(self, table_name: Any, value: Any) -> None:
        """ Метод для заполнения таблицы. """
        if isinstance(table_name, int):
            table_name = f"'{table_name}'"
        if isinstance(value, str) or isinstance(value, int):
            value = value,
        columns = ','.join('?' * len(value))
        self._cursor.execute(f"INSERT INTO {table_name} VALUES({columns})", value)
        self.commit()

    def select_table(self, table_name: Any) -> List[Tuple]:
        """ Метод для извлечения данных таблицы. """
        if isinstance(table_name, int):
            table_name = f"'{table_name}'"
        self._cursor.execute(f"SELECT * from {table_name}")
        return self._cursor.fetchall()

    def check_presence_table(self, table_name: Any) -> bool:
        """ Метод для проверки наличия таблицы в БД.
        Возвращает True если таблица уже существует в БД. """
        if isinstance(table_name, int):
            table_name = f"'{table_name}'"
        table_name = table_name,
        self._cursor.execute(f"SELECT name FROM sqlite_master WHERE name = (?)", table_name)
        return len(self._cursor.fetchall()) != 0

    def check_presence(self, table_name: Any, column_name: str, value: str) -> bool:
        """ Метод для проверки наличия значения в таблице (во избежание повторений).
        Возвращает True если значение уже есть в таблице. """
        if isinstance(table_name, int):
            table_name = f"'{table_name}'"
        if isinstance(value, tuple):
            value = value[0]
        value = value,
        self._cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {column_name} = (?)", value)
        return len(self._cursor.fetchall()) != 0

    def get_cell_value(self, table_name: Any, find_column: str, column: str, value: Any) -> List[Tuple]:
        """ Метод для получения значения ячейки. """
        value = value,
        return self._cursor.execute(f"SELECT {find_column} FROM {table_name} "
                                    f"WHERE {column} = (?)", value).fetchall()

    def commit(self) -> None:
        """ Метод для внесения изменений в БД. """
        self._connect.commit()


if __name__ == '__main__':
    ModelDb()
