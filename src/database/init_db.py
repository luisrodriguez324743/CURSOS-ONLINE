from src.database.connection import Base, engine
from src.entities.usuario import Usuario
from src.entities.rol import Rol
from src.entities.resena import Resena
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.leccion import Leccion

Base.metadata.create_all(bind=engine)
