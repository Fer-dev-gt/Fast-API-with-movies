from fastapi import FastAPI, Body, Request, HTTPException, Path, Query, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.title = "Le cambié el nombre a mi API"
app.version = "7.7.7"


Base.metadata.create_all(bind = engine)         # Acá estoy creando las tablas en la base de datos y hago la conexión con la base de datos usando el motor de la base de datos


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)
       if data['email'] != "admin@gmail.com":
           raise HTTPException(status_code=403, detail="Credentials not valid") 

    # def __init__(self, auto_error: bool = True):
    #     super(JWTBearer, self).__init__(auto_error=auto_error)

    # async def __call__(self, request: Request):
    #     credentials = await super(JWTBearer, self).__call__(request)
    #     if credentials:
    #         return credentials
    #     else:
    #         raise HTTPException(
    #             status_code=403, detail="Invalid authorization code"
    #         )


class User(BaseModel):
    username: str
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
            "title": "No title",
            "overview": "No overview",
            "year": 2022,
            "rating": 7.8,
            "category": "No category"
                }
            ]
        }
    }

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


@app.get("/", tags=["Root que yo creé"])
def message():
    return HTMLResponse('<h1 style="color:blue">¡Hola, mundo!</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:

    db = Session()                                                                      # Creo la sesión de la base de datos
    result = db.query(MovieModel).all()                                                 # Acá estoy obteniendo todos los registros de la tabla movies

    return JSONResponse(status_code=200, content=jsonable_encoder(result))              # Acá estoy retornando los registros de la tabla movies, uso jsonable_encoder para convertir los objetos de la base de datos a diccionarios


# Tabmien podemos retornar un archivo HTML para trabajarlo de forma más comoda
@app.get('/archivo-html', tags=['Estoy retornando un archivo HTML'])
def get_html():
    return FileResponse('HelloWorld.html')


@app.get('/movies/{id}', tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:

    db = Session()                                    
    
    result = db.query(MovieModel).filter(MovieModel.id == id).first()                                  # Acá estoy obteniendo el registro de la tabla movies que tenga el id que viene en la URL y lo guardo en la variable result solo el primer registro que encuentre

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found'})               # Acá estoy retornando un mensaje de error si no se encuentra el registro
    return JSONResponse(status_code = 200, content =jsonable_encoder(result))                          # Acá estoy retornando el registro de la tabla movies, uso jsonable_encoder para convertir el objeto de la base de datos a diccionario



@app.get('/movies/', tags=["movies"], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20), year: int = None ) -> List[Movie]:

    db = Session()                                                                                                  # Creo la sesión de la base de datos

    result = db.query(MovieModel).filter(MovieModel.category == category).all()                                     # Acá estoy obteniendo todos los registros de la tabla movies que tengan la categoría que viene en la URL

    if not result:
        return JSONResponse(status_code = 404, content = {'message': 'Movie not found by category'})                # Acá estoy retornando un mensaje de error si no se encuentra el registro

    return JSONResponse(status_code = 200, content = jsonable_encoder(result))                                      # Acá estoy retornando los registros de la tabla movies, uso jsonable_encoder para convertir los objetos de la base de datos a diccionarios


# Aplicando Metodos POST
@app.post('/movies', tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()                                                                                      # Creo la sesión de la base de datos
    new_movie = MovieModel(**movie.model_dump())                                                        # Acá estoy creando una instancia de la clase MovieModel con los datos que vienen en el body de la petición, el ** significa que estoy desempaquetando el diccionario
    db.add(new_movie)                                                                                   # Acá estoy agregando la instancia de la clase MovieModel a la sesión de la base de datos
    db.commit()                                                                                         # Acá estoy guardando los cambios en la base de datos

    return JSONResponse(content={'message': 'Movie created successfully'}, status_code=201)



@app.post('/login', tags=["auth"])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        try:
            token: str = create_token(user.dict())
            return JSONResponse(content={"token": token}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)


# Aplicando Metodos PUT
@app.put('/movies/{id}', tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
            return JSONResponse(content={'message': 'Movie updated successfully'}, status_code=200)
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)


@app.put('/moviesImproved/{id}', tags=['movies2'])
async def update_movie(id: int, request: Request):
    update_movie = await request.json()
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            movies[index].update(update_movie)
            return movies[index]

    raise HTTPException(status_code=404, detail="Movie not found")



# Aplicando Metodos Delete
@app.delete('/movies/{id}', tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(content={'message': 'Movie deleted successfully'}, status_code=200)
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)


@app.delete('/moviesImproved/{id}', tags=['movies2'])
async def delete_movie(id: int):
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            del movies[index]
            return {'status': 'deleted movie'}

    raise HTTPException(status_code=404, detail="Movie not found")