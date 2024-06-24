from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()
app.title = "Le cambié el nombre a mi API"
app.version = "7.7.7"

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



@app.get('/movies', tags=["movies"])
def get_movies():
    return movies



# Tabmien podemos retornar un archivo HTML para trabajarlo de forma más comoda
@app.get('/archivo-html', tags=['Estoy retornando un archivo HTML'])
def get_html():
    return FileResponse('HelloWorld.html')



@app.get('/movies/{id}', tags=["Getting a movie by id"])
def get_movie_by_id(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return {'message': 'Movie not found'}


@app.get('/movies/', tags=["Getting a movie by category"])
def get_movie_by_category(category: str, year: int = None ):
    return [movie for movie in movies if movie['category'].lower() == category.lower() and movie['year'] == year]
    # return [movie for movie in movies if movie['category'].lower() == category.lower()]
    # return category