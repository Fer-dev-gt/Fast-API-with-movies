import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sqlite_file_name = '../database.sqlite'

base_dir = os.path.dirname(os.path.realpath(__file__))                  # Acá estoy obteniendo la ruta absoluta del archivo database.py que es donde se encuentra este código  

database_url = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}'  # Acá estoy creando la URL de la base de datos que se va a utilizar en la aplicación

engine = create_engine(database_url, echo=True)                        # Acá estoy creando el motor de la base de datos que servirá para conectarse a la base de datos

Session = sessionmaker(bind=engine)                                  # Acá estoy creando la sesión de la base de datos que se va a utilizar en la aplicación

Base = declarative_base()                                             # Acá estoy creando la base de datos que se va a utilizar en la aplicación