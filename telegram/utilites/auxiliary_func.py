""" Модуль со вспомогательными функциями. """

import os
from typing import Optional
import random

from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup
import urllib
from PIL import Image
import requests

from database.core import db
from site_api.core import common_api
from telegram.utilites.inline_keyboard import InlineKeyboard


def _call_enter_actor_or_movie(bot: TeleBot, message: Message, user_id: int, message_text: str) -> str:
    """ Функция для вывода сообщения с просьбой ввести имя искомого актера/ название фильма. """
    db.check_presence_and_create_table_user_requests(user_id)
    name = message_text.split()[0].lower()
    bot.send_message(message.chat.id, f"Enter the {name}'s name:")
    return name


def _call_ratings_inline_keyboard(bot: TeleBot, message: Message, user_id: int) -> None:
    """ Функция вызова встроенной клавиатуры с выбором вида рейтинга. """
    db.check_presence_and_create_table_user_requests(user_id)
    keyboard = InlineKeyboard().ratings_inline_keyboard()(user_id)
    bot.send_message(message.chat.id, 'What rating are you looking for?', reply_markup=keyboard)


def _call_random_inline_keyboard(bot: TeleBot, message: Message, user_id: int) -> None:
    """ Функция вызова встроенной клавиатуры с выбором - где искать случайный фильм. """
    db.check_presence_and_create_table_user_requests(user_id)
    keyboard = InlineKeyboard().random_inline_keyboard()(user_id)
    bot.send_message(message.chat.id, 'You can find random movie from...', reply_markup=keyboard)


def _call_actors_or_movies_inline_keyboard(message: Message, flag: str) -> InlineKeyboard:
    """ Функция вызова встроенной клавиатуры с выбором актера/фильма. """
    name = message.text

    if flag == 'actor':
        method = common_api.ActorsByName()
    elif flag == 'movie':
        method = common_api.MovieByTitle()

    name_with_id = method.get()(name)

    for key, value in name_with_id.items():
        db.check_presence_and_insert_value_to_all_data((key, value))

    return InlineKeyboard().inline_keyboard_column()(info=name_with_id, user_id=message.from_user.id,
                                                     callback_startswith=flag)


def _fill_button_inline_keyboard(user_id: int, method: common_api, name_id: str,
                                 callback_startswith: str) -> InlineKeyboardMarkup:
    """ Функция для заполнения инлайн-кнопок. """
    name_with_id = method(name_id).get()

    for key, value in name_with_id.items():
        db.check_presence_and_insert_value_to_all_data((key, value))

    keyboard = InlineKeyboard().inline_keyboard_column()(info=name_with_id, user_id=user_id,
                                                         callback_startswith=callback_startswith)
    return keyboard


def _call_actor_or_movie_info(bot: TeleBot, message: Message, user_id: int, callback_data: str, name=None) -> None:
    """ Функция для вывода информации об актёре/фильме """
    db.check_presence_and_create_table_user_requests(user_id)

    name_id = callback_data.split()[1]

    if not name:
        name = db.get_name(name_id)
    
    db.check_presence_and_insert_value_to_requests(user_id=user_id, value=name)

    if callback_data.startswith('actor'):
        method1 = common_api.ActorInfo
        method2 = common_api.ActorMovies
        method3 = common_api.NewMoviesOfActor
        new_callback_startswith = 'movie'
    elif callback_data.startswith('movie'):
        method1 = common_api.MovieInfo
        method2 = common_api.MovieActors
        method3 = common_api.LooksLikeMovie
        new_callback_startswith = 'actor'

    info = method1(name_id).get()

    if _check_photo_size(info[1], info[2]):
        with open('temp_img.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, photo=file)
        os.remove('temp_img.jpg')
    else:
        bot.send_photo(message.chat.id, info[1])

    bot.send_message(message.chat.id, info[0])

    keyboard = _fill_button_inline_keyboard(user_id=user_id, method=method2, name_id=name_id,
                                            callback_startswith=new_callback_startswith)
    bot.send_message(message.chat.id, f'{new_callback_startswith.title()}s:', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Please wait to see more...')

    keyboard = _fill_button_inline_keyboard(user_id=user_id, method=method3, name_id=name_id,
                                            callback_startswith='movie')

    if callback_data.startswith('movie'):
        mess = 'Movies like this:'
    elif callback_data.startswith('actor'):
        mess = 'New movies of actor:'

    bot.send_message(message.chat.id, mess, reply_markup=keyboard)


def _count_top(callback_flag: str, end_top: int) -> int:
    """ Функция для ведения счёта фильмов в топе (для вывода по 10 шт. в сообщении). """
    if callback_flag == 'genre' or callback_flag == 'TOP 100':
        end_top = 10
    elif callback_flag == 'top_genre' or callback_flag == 'top_10':
        end_top += 10
    return end_top


def _check_photo_size(url: str, size: int) -> Optional[str]:
    """ Функция для проверки размера фотографии:
    в случае превышения создает временный файл с уменьшенными размерами. """
    if size > 9999:
        file = open('temp_img.jpg', 'wb')
        file.write(urllib.request.urlopen(url).read())
        file.close()
        img = Image.open('temp_img.jpg')
        img.thumbnail(size=(500, 500))
        img.save('temp_img.jpg')
        img.close()
        return 'temp_img.jpg'


def _get_random_word() -> str:
    """ Функция для получения случайного слова. """
    url = 'https://www.mit.edu/~ecprice/wordlist.10000'
    list_of_words = requests.get(url=url, timeout=5).content.decode('utf-8').splitlines()

    return random.choice(list_of_words)


class OtherFunc:

    @staticmethod
    def call_enter_actor_or_movie():
        return _call_enter_actor_or_movie

    @staticmethod
    def call_ratings_inline_keyboard():
        return _call_ratings_inline_keyboard

    @staticmethod
    def call_random_inline_keyboard():
        return _call_random_inline_keyboard

    @staticmethod
    def call_actors_or_movies_inline_keyboard():
        return _call_actors_or_movies_inline_keyboard

    @staticmethod
    def fill_button_inline_keyboard():
        return _fill_button_inline_keyboard

    @staticmethod
    def call_actor_or_movie_info():
        return _call_actor_or_movie_info

    @staticmethod
    def count_top():
        return _count_top

    @staticmethod
    def check_photo_size():
        return _check_photo_size

    @staticmethod
    def get_random_word():
        return _get_random_word


other_func = OtherFunc()


if __name__ == '__main__':
    _call_enter_actor_or_movie()
    _call_ratings_inline_keyboard()
    _call_actors_or_movies_inline_keyboard()
    _call_actor_or_movie_info()
    _count_top()
    _check_photo_size()
    _get_random_word()

    OtherFunc()
