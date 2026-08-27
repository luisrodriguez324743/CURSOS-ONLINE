from src.entities.progreso import Progreso
from .base_crud import CRUD


class ProgresoCRUD(CRUD[Progreso]):
    def __init__(self) -> None:
        super().__init__(Progreso)
