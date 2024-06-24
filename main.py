from fastapi import FastAPI, Body, Request, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Le cambié el nombre a mi API"
app.version = "7.7.7"

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



@app.get('/movies', tags=["movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)


# Tabmien podemos retornar un archivo HTML para trabajarlo de forma más comoda
@app.get('/archivo-html', tags=['Estoy retornando un archivo HTML'])
def get_html():
    return FileResponse('HelloWorld.html')


@app.get('/movies/{id}', tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie['id'] == id:
            return JSONResponse(content=movie)
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)


@app.get('/movies/', tags=["movies"], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20), year: int = None ) -> List[Movie]:
    data = [movie for movie in movies if movie['category'].lower() == category.lower() and movie['year'] == year]
    return JSONResponse(content=data)


# Aplicando Metodos POST
@app.post('/movies', tags=["movies"], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={'message': 'Movie created successfully'}, status_code=201)


# Aplicando Metodos PUT
@app.put('/movies/{id}', tags=["movies"], response_model=dict)
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



# Aplicando Metodos Delete
@app.delete('/movies/{id}', tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return {'message': 'Movie deleted'}
    return {'message': 'Movie not found'}



@app.put('/moviesImproved/{id}', tags=['movies2'])
async def update_movie(id: int, request: Request):
    update_movie = await request.json()
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            movies[index].update(update_movie)
            return movies[index]

    raise HTTPException(status_code=404, detail="Movie not found")


@app.delete('/moviesImproved/{id}', tags=['movies2'])
async def delete_movie(id: int):
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            del movies[index]
            return {'status': 'deleted movie'}

    raise HTTPException(status_code=404, detail="Movie not found")