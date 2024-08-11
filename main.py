from fastapi import FastAPI
from fastapi.responses import FileResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
app.title = "Le cambié el nombre a mi API"
app.version = "7.7.7"

app.add_middleware(ErrorHandler)                # Acá estoy añadiendo el middleware de error_handler a la aplicación
app.include_router(movie_router)                 # Acá estoy incluyendo el router de movie en la aplicación
app.include_router(user_router)                 # Acá estoy incluyendo el router de user en la aplicación

Base.metadata.create_all(bind = engine)         # Acá estoy creando las tablas en la base de datos y hago la conexión con la base de datos usando el motor de la base de datos




# Tabmien podemos retornar un archivo HTML para trabajarlo de forma más comoda
@app.get('/archivo-html', tags=['Estoy retornando un archivo HTML'])
def get_html():
    return FileResponse('HelloWorld.html')


