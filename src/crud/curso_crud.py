from src.entities.curso import Curso
from .base_crud import CRUD


class CursoCRUD(CRUD[Curso]):
    def __init__(self) -> None:
        super().__init__(Curso)
