from uuid import UUID
from src.entities.resena import Resena
from .base_crud import CRUD


class ResenaCRUD(CRUD[Resena]):
    def __init__(self) -> None:
        super().__init__(Resena)

    def obtener_por_curso(self, id_curso: UUID) -> list[Resena]:
        """Devuelve todas las reseñas pertenecientes a un curso específico."""
        return [
            resena for resena in self.registros.values() if resena.id_curso == id_curso
        ]

    def obtener_por_usuario(self, id_usuario: UUID) -> list[Resena]:
        """Devuelve todas las reseñas escritas por un usuario."""
        return [
            resena
            for resena in self.registros.values()
            if resena.id_usuario == id_usuario
        ]

    def promedio_calificacion_curso(self, id_curso: UUID) -> float:
        """Calcula el promedio de estrellas/puntuación de un curso."""
        reseñas_curso = self.obtener_por_curso(id_curso)
        if not reseñas_curso:
            return 0.0

        suma = sum(r.calificacion for r in reseñas_curso)
        return round(suma / len(reseñas_curso), 2)
