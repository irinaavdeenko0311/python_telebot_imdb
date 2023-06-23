""" Модуль для создания обычных клавиатур. """

from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def _reply_button(name: str) -> KeyboardButton:
    """ Функция для создания одной кнопки для обычной клавиатуры. """
    return types.KeyboardButton(name)


def _reply_keyboard_row(*args) -> ReplyKeyboardMarkup:
    """ Функция для создания обычной клавиатуры из кнопок в ряд. """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*args)
    return keyboard


def _main_reply_keyboard() -> ReplyKeyboardMarkup:
    """ Функция для создания обычной клавиатуры главного меню поиска. """
    name1 = _reply_button('ACTOR')
    name2 = _reply_button('MOVIE')
    name3 = _reply_button('TOP MOVIES')
    name4 = _reply_button('RANDOM MOVIE')
    keyboard = _reply_keyboard_row(name1, name2)
    return keyboard.row(name3, name4)


class ReplyKeyboard:
    @staticmethod
    def reply_button():
        return _reply_button

    @staticmethod
    def reply_keyboard_row():
        return _reply_keyboard_row

    @staticmethod
    def main_reply_keyboard():
        return _main_reply_keyboard


reply_keyboard = ReplyKeyboard()


if __name__ == '__main__':
    _reply_button()
    _reply_keyboard_row()
    _main_reply_keyboard()

    ReplyKeyboard()

