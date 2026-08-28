from src.entities.pago import Pago
from .base_crud import CRUD


class PagoCRUD(CRUD[Pago]):
    def __init__(self) -> None:
        super().__init__(Pago)
