from src.entities.leccion import Leccion
from .base_crud import CRUD


class LeccionCRUD(CRUD[Leccion]):
    def __init__(self) -> None:
        super().__init__(Leccion)
