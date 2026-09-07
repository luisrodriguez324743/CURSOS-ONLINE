from database.connection import Base, engine
from entities.usuario import Usuario
from entities.rol import Rol
from entities.resena import Resena



Base.metadata.create_all(bind=engine)