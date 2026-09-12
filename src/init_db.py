import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import Base, engine
from src.entities.certificado import Certificado
from src.entities.factura import Factura
from src.entities.pago import Pago

Base.metadata.create_all(bind=engine)
