import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import Base, engine
from src.database.schema import remove_empty_legacy_tables
from src.entities.certificado import Certificado
from src.entities.factura import Factura
from src.entities.pago import Pago
from src.entities.evaluacion import Evaluacion
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso
from src.entities.usuario import Usuario
from src.entities.rol import Rol
from src.entities.resena import Resena
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.leccion import Leccion

remove_empty_legacy_tables()
Base.metadata.create_all(bind=engine)
