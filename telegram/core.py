""" Основной модуль в боте: вывод информации и обработка сообщений. """

import random

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from settings import SiteSettings

from telegram.utilites.inline_keyboard import inline_keyboard
from telegram.utilites.reply_keyboard import reply_keyboard

from telegram.utilites.auxiliary_func import other_func
from database.core import db
from site_api.core import common_api

site = SiteSettings()

my_bot = TeleBot(site.api_token.get_secret_value())
db.check_presence_and_create_table_users_id()
db.check_presence_and_create_table_all_data()

callback_flag = None
end_top_100 = 10
end_top_genre = 10


""" Команды """


@my_bot.message_handler(commands=['start'])
def starting(message: Message):
    """ Обработка команды /start. Выводит приветственное сообщение и меню."""
    db.check_presence_and_create_table_user_requests(message.from_user.id)

    my_bot.send_message(message.chat.id, 'Hello!')

    keyboard = inline_keyboard.main_inline_keyboard()(message.from_user.id)
    my_bot.send_message(message.chat.id, 'What are you looking for?', reply_markup=keyboard)


@my_bot.message_handler(commands=['buttons'])    
def main_buttons(message: Message):
    """ Обработка команды /buttons. Выводит главное меню."""
    db.check_presence_and_create_table_user_requests(message.from_user.id)

    keyboard = reply_keyboard.main_reply_keyboard()()
    my_bot.send_message(message.chat.id, 'You can find:', reply_markup=keyboard)


@my_bot.message_handler(commands=['history'])
def call_history(message: Message):
    """ Обработка команды /history. Выводит историю запросов пользователя. """
    db.check_presence_and_create_table_user_requests(message.from_user.id)

    history = db.select_table(table_name=message.from_user.id)
    history = '\n'.join([i[0] for i in history])
    my_bot.send_message(message.chat.id, f'Search history:\n{history}')


""" Запросы обратного вызова: """


@my_bot.callback_query_handler(
    func=lambda callback: callback.data.startswith('ACTOR') or callback.data.startswith('MOVIE')
)
def callback_actor_or_movie(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопки выбора актера или фильма. """
    user_id = int(callback.data.split()[-1])

    global callback_flag
    callback_flag = other_func.call_enter_actor_or_movie()(bot=my_bot, message=callback.message,
                                                           user_id=user_id, message_text=callback.data)


@my_bot.callback_query_handler(func=lambda callback: callback.data.startswith('TOP MOVIES'))
def callback_top_movies(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку выбора рейтинга. """
    user_id = int(callback.data.split()[-1])
    other_func.call_ratings_inline_keyboard()(bot=my_bot, message=callback.message, user_id=user_id)


@my_bot.callback_query_handler(func=lambda callback: callback.data.startswith('RANDOM MOVIE'))
def callback_random(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку выбора случайного фильма. """
    user_id = int(callback.data.split()[-1])
    other_func.call_random_inline_keyboard()(bot=my_bot, message=callback.message, user_id=user_id)


@my_bot.callback_query_handler(
    func=lambda callback: callback.data.startswith('TOP 100') or callback.data.startswith('top_10')
)
def callback_top_100(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку 'Топ 100'. """
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)
    db.check_presence_create_and_insert_table_top_100()

    top = db.select_table('top_100')
    for i in top:
        db.check_presence_and_insert_value_to_all_data((i[0], i[1]))

    global end_top_100
    end_top_100 = other_func.count_top()(callback_flag=' '.join(callback.data.split()[:-1]), end_top=end_top_100)

    keyboard = inline_keyboard.inline_keyboard_top_10_column()(
        info=top, user_id=user_id, end=end_top_100, flag=' '.join(callback.data.split()[:-1])
    )

    my_bot.send_message(callback.message.chat.id, 'Top 100:', reply_markup=keyboard)

    if end_top_100 == 100:
        end_top_100 = 10


@my_bot.callback_query_handler(func=lambda callback: callback.data.startswith('POPULAR TODAY'))
def callback_popular_movies(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку популярных сегодня. """
    my_bot.send_message(callback.message.chat.id, 'Please wait...')
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)

    movies_id_by_popular = common_api.PopularMoviesToday().get_popular_movies()
    movies_by_popular = [(i, common_api.MovieName(i).get()) for i in movies_id_by_popular]

    for i in movies_by_popular:
        db.check_presence_and_insert_value_to_all_data((i[0], i[1]))

    keyboard = inline_keyboard.inline_keyboard_top_10_column()(info=movies_by_popular, user_id=user_id, end=10)

    my_bot.send_message(callback.message.chat.id, 'Popular movies today:', reply_markup=keyboard)


@my_bot.callback_query_handler(func=lambda callback: callback.data.startswith('POPULAR MOVIES BY GENRE'))
def callback_genres(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку поиска по жанрам. """
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)
    db.check_presence_create_and_insert_table_movie_genres()

    genres = db.select_table('movie_genres')
    keyboard = inline_keyboard.inline_keyboard_genres_row()
    keyboard = keyboard(info=genres, user_id=user_id, callback_startswith='genre')
    my_bot.send_message(callback.message.chat.id, 'Genres:', reply_markup=keyboard)


@my_bot.callback_query_handler(
    func=lambda callback: callback.data.startswith('genre') or callback.data.startswith('top_genre')
)
def callback_movies_in_genre(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку жанра. """
    my_bot.send_message(callback.message.chat.id, 'Please wait...')
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)

    genre = callback.data.split()[1]
    if '-' in genre:
        genre = genre.replace('-', '_')

    db.check_presence_create_and_insert_table_movies_by_genre(genre)

    global end_top_genre
    end_top_genre = other_func.count_top()(callback_flag=callback.data.split()[0], end_top=end_top_genre)

    movies_id_by_genre = db.select_table(genre)

    movies_by_genre = [(i[0], common_api.MovieName(i[0]).get())
                       for i in movies_id_by_genre[end_top_genre - 10: end_top_genre]]

    for i in movies_by_genre:
        db.check_presence_and_insert_value_to_all_data((i[0], i[1]))

    keyboard = inline_keyboard.inline_keyboard_top_10_column()(
        info=movies_by_genre, user_id=user_id, end=end_top_genre, flag=callback.data.split()[0], genre_flag=genre
    )

    my_bot.send_message(callback.message.chat.id, f'Top movies in genre "{callback.data.split()[1].title()}":', reply_markup=keyboard)

    if end_top_genre == 30:
        end_top_genre = 10


@my_bot.callback_query_handler(
    func=lambda callback: callback.data.startswith('actor') or callback.data.startswith('movie')
)
def callback_actor_or_movie_info(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на кнопку конкретного актера/фильма. """
    my_bot.send_message(callback.message.chat.id, 'Please wait...')
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)

    other_func.call_actor_or_movie_info()(bot=my_bot, message=callback.message,
                                          user_id=user_id, callback_data=callback.data)

    global callback_flag
    callback_flag = None


@my_bot.callback_query_handler(func=lambda callback: callback.data.startswith('RANDOM'))
def callback_random_movie(callback: CallbackQuery) -> None:
    """ Функция для обработки входящего запроса обратного вызова при нажатии на выбор - где искать случайный фильм. """
    my_bot.send_message(callback.message.chat.id, 'Please wait...')
    user_id = int(callback.data.split()[-1])
    db.check_presence_and_create_table_user_requests(user_id)

    if callback.data.startswith('RANDOM TOP 100'):
        db.check_presence_create_and_insert_table_top_100()

        random_movie = random.choice(db.select_table('top_100'))
        random_movie_id = random_movie[0]
        random_movie_name = random_movie[1]

    elif callback.data.startswith('RANDOM POPULAR TODAY'):
        random_movie_id = common_api.PopularMoviesToday().get_random_movie()
        random_movie_name = common_api.MovieName(random_movie_id).get()

    elif callback.data.startswith('RANDOM ALL MOVIES'):
        random_word = other_func.get_random_word()()
        random_movie = random.choice([(k, v) for k, v in common_api.MovieByTitle().get()(random_word).items()])
        random_movie_id = random_movie[0]
        random_movie_name = random_movie[1]

    callback_data = f'movie {random_movie_id} {user_id}'
    other_func.call_actor_or_movie_info()(bot=my_bot, message=callback.message, user_id=user_id,
                                          callback_data=callback_data, name=random_movie_name)


""" Текстовые сообщения: """


@my_bot.message_handler(func=lambda message: message.text == 'ACTOR' or message.text == 'MOVIE')
def message_actor_or_movie(message: Message) -> None:
    """ Функция для обработки входящих сообщений в ответ на нажатие кнопок главного меню - поиск актера/фильма. """
    global callback_flag
    callback_flag = other_func.call_enter_actor_or_movie()(bot=my_bot, message=message,
                                                           user_id=message.from_user.id, message_text=message.text)


@my_bot.message_handler(func=lambda message: message.text == 'TOP MOVIES')
def message_top_movies(message: Message) -> None:
    """ Функция для обработки входящих сообщений в ответ на нажатие кнопок главного меню - поиск рейтингов. """
    other_func.call_ratings_inline_keyboard()(bot=my_bot, message=message, user_id=message.from_user.id)


@my_bot.message_handler(func=lambda message: message.text == 'RANDOM MOVIE')
def message_random_movie(message: Message) -> None:
    """ Функция для обработки входящих сообщений в ответ на нажатие кнопок главного меню - случайный фильм. """
    other_func.call_random_inline_keyboard()(bot=my_bot, message=message, user_id=message.from_user.id)


@my_bot.message_handler()
def message_reply(message: Message):
    """ Функция для обработки остальных входящих сообщений. """
    db.check_presence_and_create_table_user_requests(message.from_user.id)

    if callback_flag == 'actor' or callback_flag == 'movie':
        my_bot.send_message(message.chat.id, 'Please wait...')
        keyboard = other_func.call_actors_or_movies_inline_keyboard()(message=message, flag=callback_flag)
        my_bot.send_message(message.chat.id, f'{callback_flag.title()}s:', reply_markup=keyboard)

    else:
        keyboard = inline_keyboard.main_inline_keyboard()(message.from_user.id)
        my_bot.send_message(message.chat.id, 'What are you looking for?', reply_markup=keyboard)


if __name__ == '__main__':
    my_bot.infinity_polling()
