from src.database.connection import Base, engine
from src.database.schema import remove_empty_legacy_tables
from src.entities.usuario import Usuario
from src.entities.rol import Rol
from src.entities.resena import Resena
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.leccion import Leccion
from src.entities.factura import Factura
from src.entities.pago import Pago
from src.entities.certificado import Certificado
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso
from src.entities.evaluacion import Evaluacion


def init_db():
    print("Creando tablas faltantes en la base de datos...")
    remove_empty_legacy_tables()
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas o verificadas correctamente.")


if __name__ == "__main__":
    init_db()
