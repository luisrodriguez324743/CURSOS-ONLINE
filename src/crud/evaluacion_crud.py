from src.entities.evaluacion import Evaluacion
from .base_crud import CRUD


class EvaluacionCRUD(CRUD[Evaluacion]):
    def __init__(self) -> None:
        super().__init__(Evaluacion)
