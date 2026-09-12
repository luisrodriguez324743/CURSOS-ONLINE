from src.database.connection import Base, engine

from src.entities.certificado import Certificado
from src.entities.curso import Curso
from src.entities.evaluacion import Evaluacion
from src.entities.factura import Factura
from src.entities.inscripcion import Inscripcion
from src.entities.leccion import Leccion
from src.entities.modulo import Modulo
from src.entities.pago import Pago
from src.entities.progreso import Progreso
from src.entities.resena import Resena
from src.entities.rol import Rol
from src.entities.usuario import Usuario


def init_db() -> None:
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas correctamente!")

if __name__ == "__main__":
    init_db()