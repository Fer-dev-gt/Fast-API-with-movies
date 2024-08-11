from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from fastapi.responses import HTMLResponse
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter() 


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Titanic',
        'overview': "Jack (Leonardo DiCaprio) es un joven artista que, en una partida de cartas, gana un pasaje para ...",
        'year': 1997,
        'rating': 7.8,
        'category': 'Romance'    
    },
    {
        'id': 3,
        'title': 'Star Wars: Episodio VII - El despertar de la Fuerza',
        'overview': "Treinta años después de la victoria de la Alianza Rebelde sobre la segunda Estrella de la Muerte ...",
        'year': 2015,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 4,
        'title': 'Avengers: Endgame',
        'overview': "Después de los eventos devastadores de Avengers: Infinity War, el universo está en ruinas debido a las acciones de Thanos ...",
        'year': 2019,
        'rating': 8.4,
        'category': 'Acción'    
    },
    {
        'id': 5,
        'title': 'Jurassic Park',
        'overview': "El multimillonario John Hammond consigue hacer realidad su sueño de clonar dinosaurios ...",
        'year': 1993,
        'rating': 7.9,
        'category': 'Ciencia Ficción'    
    },
    {
        'id': 6,
        'title': 'The Lion King',
        'overview': "Un joven león llamado Simba, príncipe de la sabana, verá su vida cambiada cuando su malvado tío Scar ...",
        'year': 1994,
        'rating': 8.5,
        'category': 'Animación'    
    },
    {
        'id': 7,
        'title': 'The Dark Knight',
        'overview': "Batman/Bruce Wayne (Christian Bale) regresa para continuar su guerra contra el crimen ...",
        'year': 2008,
        'rating': 9.0,
        'category': 'Acción'    
    },
]



@movie_router.get("/", tags=["Root que yo creé"])
def message():
    return HTMLResponse('<h1 style="color:blue">¡Hola, mundo!</h1>')


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:

    db = Session()                                                                      # Creo la sesión de la base de datos
    result = MovieService(db).get_movies()                                              # Acá estoy obteniendo todos los registros de la tabla movies

    return JSONResponse(status_code=200, content=jsonable_encoder(result))              # Acá estoy retornando los registros de la tabla movies, uso jsonable_encoder para convertir los objetos de la base de datos a diccionarios




@movie_router.get('/movies/{id}', tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:

    db = Session()                                    
    
    result = MovieService(db).get_movie(id)                                                              # Acá estoy obteniendo el registro de la tabla movies que tenga el id que viene en la URL

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found'})               # Acá estoy retornando un mensaje de error si no se encuentra el registro
    return JSONResponse(status_code = 200, content =jsonable_encoder(result))                          # Acá estoy retornando el registro de la tabla movies, uso jsonable_encoder para convertir el objeto de la base de datos a diccionario



@movie_router.get('/movies/', tags=["movies"], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20), year: int = None ) -> List[Movie]:

    db = Session()                                                                                                  # Creo la sesión de la base de datos

    result = MovieService(db).get_movie_by_category(category)                                                        # Acá estoy obteniendo los registros de la tabla movies que tengan la categoría que viene en la URL

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found by category'})                # Acá estoy retornando un mensaje de error si no se encuentra el registro

    return JSONResponse(status_code = 200, content = jsonable_encoder(result))                                      # Acá estoy retornando los registros de la tabla movies, uso jsonable_encoder para convertir los objetos de la base de datos a diccionarios


# Aplicando Metodos POST
@movie_router.post('/movies', tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()                                                                                      # Creo la sesión de la base de datos

    MovieService(db).create_movie(movie)                                                               # Acá estoy creando un nuevo registro en la tabla movies

    return JSONResponse(content={'message': 'Movie created successfully'}, status_code=201)



# Aplicando Metodos PUT
@movie_router.put('/movies/{id}', tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    db = Session()                                                                                      # Creo la sesión de la base de datos
    result = MovieService(db).get_movie(id)                                                             # Acá estoy obteniendo el registro de la tabla movies que tenga el id que viene en la URL

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found'})                # Acá estoy retornando un mensaje de error si no se encuentra el registro
    
    MovieService(db).update_movie(id, movie)                                                           # Acá estoy actualizando el registro de la tabla movies

    db.commit()                                                                                         # Acá estoy guardando los cambios en la base de datos
    db.refresh(result)                                                                                  # Acá estoy refrescando el registro

    return JSONResponse(status_code=200, content={'message': 'Movie updated successfully'})             # Acá estoy retornando un mensaje de éxito


@movie_router.put('/moviesImproved/{id}', tags=['movies2'])
async def update_movie(id: int, request: Request):
    update_movie = await request.json()
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            movies[index].update(update_movie)
            return movies[index]

    raise HTTPException(status_code=404, detail="Movie not found")



# Aplicando Metodos Delete
@movie_router.delete('/movies/{id}', tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()                                                                                      # Creo la sesión de la base de datos
    result : MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()                      # Acá estoy obteniendo el registro de la tabla movies que tenga el id que viene en la URL

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found'})                # Acá estoy retornando un mensaje de error si no se encuentra el registro
    
    MovieService(db).delete_movie(id)                                                                  # Acá estoy eliminando el registro de la tabla movies

    return JSONResponse(content={'message': 'Movie deleted successfully'}, status_code=200)             # Acá estoy retornando un mensaje de éxito


@movie_router.delete('/moviesImproved/{id}', tags=['movies2'])
async def delete_movie(id: int):
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            del movies[index]
            return {'status': 'deleted movie'}

    raise HTTPException(status_code=404, detail="Movie not found")