from src.entities.inscripcion import Inscripcion
from .base_crud import CRUD


class InscripcionCRUD(CRUD[Inscripcion]):
    def __init__(self) -> None:
        super().__init__(Inscripcion)
