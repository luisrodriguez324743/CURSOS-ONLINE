from src.entities.modulo import Modulo
from .base_crud import CRUD


class ModuloCRUD(CRUD[Modulo]):
    def __init__(self) -> None:
        super().__init__(Modulo)
