from models.movie import Movie as MovieModel
from schemas.movie import Movie as MovieSchema


class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    

    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.name == category).all()
        return result
    

    def create_movie(self, movie: MovieSchema):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()

        return new_movie

    
    def update_movie(self, id: int, data: MovieSchema):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return movie
    

    def delete_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie)
        self.db.commit()
        return movie