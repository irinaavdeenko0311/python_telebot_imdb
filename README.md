Телеграм-бот для поиска актеров и фильмов.

Название: IMDb_bot @IrinaAvdeenkoBot.

Начало работы:

В файле .env необходимо вставить свои ключи:
API_TOKEN - чтобы его получить в telegram обращаемся к боту BotFather, регистрируем новый бот (/newbot) и получаем API Token.

API_KEY - на сайте https://rapidapi.com войти в свой аккаунт (либо зарегистрировать). Далее получить свой ключ "X-RapidAPI-Key" (в любом API). В программе используется два API: https://rapidapi.com/apidojo/api/online-movie-database и https://rapidapi.com/rapihub-rapihub-default/api/imdb-top-100-movies . Если потребуется, по этим ссылкам можно подписаться, нажав кнопку "Subscribe to Test". Далее выбрать бесплатный план "Basic". Ключ появится в коде справа в словаре "headers".

Информация обрабатывается с помощью базы данных. Изменить её имя можно в модуле database/core.py - переменная name_db.

Запуск кода производится из файла main.py.

Как работает бот:

Для выбора способа поиска нажмите команду /start либо /button.

- Информация об актере:

При выборе кнопки 'ACTOR' необходимо ввести имя актера. После этого будут найдены актеры с таким именем - необходимо выбрать нужного. Далее будет показана информация об актере: фото, описание; будут выведены фильмы с участием актера в виде кнопок - нажав на одну из них получите информации о фильме; будут выведены свежие фильмы, в которых актер снялся.

- Информация о фильме:

При выборе кнопки 'MOVIE' необходимо ввести название фильма. После этого будут найдены фильмы с таким названием - необходимо выбрать нужный. Далее будет показана информация о фильме: постер, описание; будут выведены актеры, играющие главные роли в фильме, в виде кнопок - нажав на одну из них получите информацию об актере; будут выведены фильмы, похожие на этот.

- Рейтинги:

При выборе кнопки 'TOP MOVIES' будет предложен выбор - посмотреть Топ 100 фильмов ('TOP 100'), посмотреть топ популярных сегодня ('POPULAR TODAY') либо найти рейтинг популярных фильмов в жанре ('POPULAR MOVIES BY GENRE').

При выборе кнопки 'TOP 100' будет выведен список из десяти первых фильмов Топа (в виде кнопок - нажав на одну из них получите информацию о фильме); также в конце добавлена кнопка '>>>see more>>>', нажав на которую показывает следующие 10 фильмов в топе - и так до конца рейтинга.

При выборе кнопки 'POPULAR TODAY' будет выведен список из десяти фильмов, популярных сегодня (в виде кнопок - нажав на одну из них получите информацию о фильме).

При выборе кнопки 'POPULAR MOVIES BY GENRE' будет выведен список возможных жанров в виде кнопок - нажав на одну из них будет выведен список из десяти популярных фильмов в данном жанре (в виде кнопок - нажав на одну из них получите информацию о фильме); также в конце добавлена кнопка '>>>see more>>>', нажав на которую показывает следующие 10 фильмов в топе (до 30 шт.).

- Случайный фильм:

При выборе кнопки 'RANDOM MOVIE' будет предложен выбор - найти случайный фильм из Топ 100 ('TOP 100'), найти случайный фильм из популярных сегодня ('POPULAR TODAY') либо найти случайный фильм из всех существующих в мире ('ALL MOVIES')

При выборе любой из кнопок будет выведена информация о фильме.

Команда /history - показывает историю запросов пользователя (информацию о каких актерах и фильмах смотрел).