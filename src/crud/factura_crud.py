from src.entities.factura import Factura
from .base_crud import CRUD


class FacturaCRUD(CRUD[Factura]):
    def __init__(self) -> None:
        super().__init__(Factura)
