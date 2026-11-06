from sqlalchemy import inspect, text

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
    constraint_name = "uq_certificado_usuario_curso"
    constraints = inspect(engine).get_unique_constraints("certificado")
    if not any(constraint.get("name") == constraint_name for constraint in constraints):
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE certificado "
                    "ADD CONSTRAINT uq_certificado_usuario_curso "
                    "UNIQUE (id_usuario, id_curso)"
                )
            )
    print("¡Tablas creadas correctamente!")


if __name__ == "__main__":
    init_db()
