from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.evaluacion import Evaluacion
from src.entities.leccion import Leccion
from src.entities.modulo import Modulo
from src.entities.curso import Curso
from .base_crud import CRUD


class EvaluacionCRUD(CRUD[Evaluacion]):
    """
    CRUD encargado de gestionar las evaluaciones
    realizadas por los usuarios.
    """

    def __init__(self) -> None:
        super().__init__(Evaluacion)

    def crear(self, registro: Evaluacion) -> Evaluacion:
        """Registra una nueva evaluación."""
        if registro is None:
            raise ValueError("La evaluación no puede ser nula.")
        if not registro.nombre or not registro.nombre.strip():
            raise ValueError("La evaluación debe tener un nombre.")
        if registro.calificacion < 0 or registro.calificacion > 100:
            raise ValueError("La calificación debe estar entre 0 y 100.")

        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo guardar la evaluación.") from exc
        finally:
            session.close()

    def listar(self) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones registradas."""
        return super().listar()

    def listar_por_curso(self, id_curso: UUID) -> list[Evaluacion]:
        session = get_session()
        try:
            return (
                session.query(Evaluacion)
                .join(Leccion, Evaluacion.id_leccion == Leccion.id_leccion)
                .join(Modulo, Leccion.id_modulo == Modulo.id_modulo)
                .join(Curso, Modulo.id_curso == Curso.id_curso)
                .filter(Curso.id_curso == id_curso)
                .all()
            )
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Evaluacion | None:
        """Obtiene una evaluación mediante su identificador."""
        return super().obtener(identificador)

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Evaluacion | None:
        """Actualiza los datos de una evaluación existente."""
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        """Elimina una evaluación mediante su identificador."""
        return super().eliminar(identificador)
