from src.database.connection import Base, engine
from src.entities.usuario import Usuario
from src.entities.rol import Rol
from src.entities.resena import Resena
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.leccion import Leccion

def init_db():
    print("⚠️ Eliminando tablas antiguas en Neon DB...")
    Base.metadata.drop_all(bind=engine)  # Elimina las tablas para limpiar el esquema viejo
    
    print("✨ Creando tablas actualizadas...")
    Base.metadata.create_all(bind=engine) # Crea todas las tablas con sus columnas y FKs correctas
    print("✅ Tablas creadas con éxito.")

if __name__ == "__main__":
    init_db()
