""" Модуль для создания встроенных клавиатур. """

from typing import Dict, List

from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def _inline_button(user_id: int, value: str, callback_startswith: str, key=None) -> InlineKeyboardButton:
    """ Функция для создания одной кнопки для встроенной клавиатуры. """
    if key:
        return types.InlineKeyboardButton(text=value, callback_data=f'{callback_startswith} {key} {user_id}')
    else:
        return types.InlineKeyboardButton(text=value, callback_data=f'{callback_startswith} {user_id}')


def _inline_keyboard_row(*args) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры из кнопок в ряд. """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*args)
    return keyboard


def _inline_keyboard_column(info: Dict, user_id: int, callback_startswith: str) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры из кнопок в столбик. """
    keyboard = types.InlineKeyboardMarkup()
    for key, value in info.items():
        button = _inline_button(user_id=user_id, value=value, callback_startswith=callback_startswith, key=key)
        keyboard.add(button)

    return keyboard


def _main_inline_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры главного меню поиска. """
    name1 = _inline_button(user_id=user_id, value='ACTOR', callback_startswith='ACTOR')
    name2 = _inline_button(user_id=user_id, value='MOVIE', callback_startswith='MOVIE')
    name3 = _inline_button(user_id=user_id, value='TOP MOVIES', callback_startswith='TOP MOVIES')
    name4 = _inline_button(user_id=user_id, value='RANDOM MOVIE', callback_startswith='RANDOM MOVIE')
    keyboard = _inline_keyboard_row(name1, name2)
    return keyboard.row(name3, name4)


def _ratings_inline_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры с выбором вида рейтинга. """
    rating1 = _inline_button(user_id=user_id, value='TOP 100', callback_startswith='TOP 100')
    rating2 = _inline_button(user_id=user_id, value='POPULAR TODAY', callback_startswith='POPULAR TODAY')
    rating3 = _inline_button(user_id=user_id, value='POPULAR MOVIES BY GENRE', callback_startswith='POPULAR MOVIES BY GENRE')
    keyboard = _inline_keyboard_row(rating1, rating2)
    return keyboard.row(rating3)


def _random_inline_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры с выбором - где искать случайный фильм. """
    random1 = _inline_button(user_id=user_id, value='TOP 100', callback_startswith='RANDOM TOP 100')
    random2 = _inline_button(user_id=user_id, value='POPULAR TODAY', callback_startswith='RANDOM POPULAR TODAY')
    random3 = _inline_button(user_id=user_id, value='ALL MOVIES', callback_startswith='RANDOM ALL MOVIES')
    return _inline_keyboard_row(random1, random2, random3)


def _inline_keyboard_genres_row(info: List, user_id: int, callback_startswith: str) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры из кнопок по три в ряд. """
    keyboard = types.InlineKeyboardMarkup()
    for i in range(0, (len(info) - len(info) % 3), 3):
        button_left = _inline_button(user_id=user_id, value=info[i][0],
                                     callback_startswith=callback_startswith,
                                     key=info[i][0].lower())
        button_med = _inline_button(user_id=user_id, value=info[i+1][0],
                                    callback_startswith=callback_startswith,
                                    key=info[i+1][0].lower())
        button_right = _inline_button(user_id=user_id, value=info[i+2][0],
                                      callback_startswith=callback_startswith,
                                      key=info[i+2][0].lower())
        keyboard.row(button_left, button_med, button_right)

    if len(info) % 3 != 0:
        last_button = _inline_button(user_id=user_id, value=info[len(info) - 1][0],
                                     callback_startswith=callback_startswith,
                                     key=(info[len(info) - 1])[0].lower())
        if len(info) % 3 == 1:
            keyboard.add(last_button)
        elif len(info) % 3 == 2:
            button_last_left = _inline_button(user_id=user_id, value=info[len(info) - 2][0],
                                              callback_startswith=callback_startswith,
                                              key=(info[len(info) - 2])[0].lower())
            keyboard.add(button_last_left, last_button)

    return keyboard


def _inline_keyboard_top_10_column(info: List, user_id: int, end: int, callback_startswith='movie',
                                   flag=None, genre_flag=None, count_limit=0) -> InlineKeyboardMarkup:
    """ Функция для создания встроенной клавиатуры в столбик из кнопок с подсчетом. """
    keyboard = types.InlineKeyboardMarkup()
    start = end - 10

    if len(info) > 10:
        for i in range(start, end):
            key = info[i][0]
            value = info[i][1]
            button = _inline_button(
                user_id=user_id, value=f'{i+1}. {value}', callback_startswith=callback_startswith, key=key
            )
            keyboard.add(button)
    else:
        for i in range(len(info)):
            key = info[i][0]
            value = info[i][1]
            button = _inline_button(
                user_id=user_id, value=f'{start + i + 1}. {value}', callback_startswith=callback_startswith, key=key
            )
            keyboard.add(button)

    if flag == 'TOP 100' or flag == 'top_10':
        callback_flag = 'top_10'
        count_limit = 100
    elif flag == 'genre' or flag == 'top_genre':
        callback_flag = 'top_genre'
        count_limit = 30

    if end < count_limit:
        if genre_flag:
            button = InlineKeyboard().inline_button()(
                user_id=user_id, value='>>> see more >>>', callback_startswith=callback_flag, key=genre_flag
            )
        else:
            button = InlineKeyboard().inline_button()(
                user_id=user_id, value='>>> see more >>>', callback_startswith=callback_flag
        )
        keyboard.add(button)

    return keyboard


class InlineKeyboard:
    @staticmethod
    def inline_button():
        return _inline_button

    @staticmethod
    def inline_keyboard_row():
        return _inline_keyboard_row

    @staticmethod
    def inline_keyboard_column():
        return _inline_keyboard_column

    @staticmethod
    def main_inline_keyboard():
        return _main_inline_keyboard

    @staticmethod
    def ratings_inline_keyboard():
        return _ratings_inline_keyboard

    @staticmethod
    def random_inline_keyboard():
        return _random_inline_keyboard

    @staticmethod
    def inline_keyboard_genres_row():
        return _inline_keyboard_genres_row

    @staticmethod
    def inline_keyboard_top_10_column():
        return _inline_keyboard_top_10_column


inline_keyboard = InlineKeyboard()


if __name__ == '__main__':
    _inline_button()
    _inline_keyboard_row()
    _inline_keyboard_column()
    _main_inline_keyboard()
    _ratings_inline_keyboard()
    _inline_keyboard_genres_row()
    _inline_keyboard_top_10_column()

    InlineKeyboard()
