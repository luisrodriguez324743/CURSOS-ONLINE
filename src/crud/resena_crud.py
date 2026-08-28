from src.entities.resena import Resena
from .base_crud import CRUD


class ResenaCRUD(CRUD[Resena]):
    def __init__(self) -> None:
        super().__init__(Resena)
