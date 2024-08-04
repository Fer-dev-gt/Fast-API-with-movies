from config.database import Base
from sqlalchemy import Column, Integer, String, Float


class Movie(Base):                                                  # Acá estoy creando la clase Movie que hereda de Base lo que significa que es un modelo de la base de datos

    __tablename__ = 'movies'                                        # Acá estoy creando el nombre de la tabla en la base de datos

    id = Column(Integer, primary_key = True, index = True)          # Acá estoy creando la columna id de tipo entero, clave primaria y con índice
    title = Column(String, nullable = False)                        # Acá estoy creando la columna title de tipo cadena de texto y no puede ser nula
    overview = Column(String, nullable = False)                     # Acá estoy creando la columna overview de tipo cadena de texto y no puede ser nula
    year = Column(Integer, nullable = False)                        # Acá estoy creando la columna year de tipo entero y no puede ser nula
    rating = Column(Float, nullable = False)                        # Acá estoy creando la columna rating de tipo flotante y no puede ser nula
    category = Column(String, nullable = False)                     # Acá estoy creando la columna category de tipo cadena de texto y no puede ser nula