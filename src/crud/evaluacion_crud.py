from typing import Any
from uuid import UUID
from src.entities.evaluacion import Evaluacion
from .base_crud import CRUD

class EvaluacionCRUD(CRUD[Evaluacion]):
    """
    CRUD encargado de gestionar las evaluaciones realizadas por los usuarios.
    """
    def __init__(self) -> None:
        super().__init__(Evaluacion)

    def crear(self, registro: Evaluacion) -> Evaluacion:
        return super().crear(registro)

    def listar(self) -> list[Evaluacion]:
        return super().listar()

    def obtener(self, identificador: UUID) -> Evaluacion | None:
        return super().obtener(identificador)

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Evaluacion | None:
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        return super().eliminar(identificador)