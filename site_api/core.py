from site_api.utilites.site_api_handler_actors import ActorsByName, ActorInfo, ActorMovies, NewMoviesOfActor
from site_api.utilites.site_api_handler_movies import MovieByTitle, MovieInfo, MovieActors, LooksLikeMovie
from site_api.utilites.site_api_handler_ratings import Top100, GenresList, MoviesByGenre, MovieName, PopularMoviesToday


class CommonApi:
    """ Общий класс, объединяющий все классы-обработчики конечных точек API.
     Цель - удобство импортирования. """

    class ActorsByName(ActorsByName):
        def get(self):
            return self.get_actors_with_id

    class ActorInfo(ActorInfo):
        def get(self):
            return self.get_info_about_actor()

    class ActorMovies(ActorMovies):
        def get(self):
            return self.get_actor_movies_with_id()

    class NewMoviesOfActor(NewMoviesOfActor):
        def get(self):
            return self.get_new_movies()

    class MovieByTitle(MovieByTitle):
        def get(self):
            return self.get_movies_with_id

    class MovieInfo(MovieInfo):
        def get(self):
            return self.get_info_about_movie()

    class MovieActors(MovieActors):
        def get(self):
            return self.get_movie_actors_with_id()

    class LooksLikeMovie(LooksLikeMovie):
        def get(self):
            return self.get_movies_looks_like()

    class Top100(Top100):
        def get(self):
            return self.get_top_100()

    class GenresList(GenresList):
        def get(self):
            return self.get_genres()

    class MoviesByGenre(MoviesByGenre):
        def get(self):
            return self.get_movies_by_genre()

    class MovieName(MovieName):
        def get(self):
            return self.get_movie_name()

    class PopularMoviesToday(PopularMoviesToday):
        pass


common_api = CommonApi()

if __name__ == '__main__':
    CommonApi()
