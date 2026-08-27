from src.entities.certificado import Certificado
from .base_crud import CRUD


class CertificadoCRUD(CRUD[Certificado]):
    def __init__(self) -> None:
        super().__init__(Certificado)
