from src.entities.rol import Rol
from .base_crud import CRUD


class RolCRUD(CRUD[Rol]):
    def __init__(self) -> None:
        super().__init__(Rol)
