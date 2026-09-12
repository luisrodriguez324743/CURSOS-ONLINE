from uuid import UUID
from sqlalchemy import func
from src.database.connection import get_session
from src.entities.resena import Resena


class ResenaCRUD:
    def crear(
        self,
        calificacion: int,
        id_usuario: UUID,
        id_curso: UUID,
        comentario: str | None = None,
    ) -> Resena:
        session = get_session()
        try:
            resena = Resena(
                calificacion=calificacion,
                comentario=comentario,
                id_usuario=id_usuario,
                id_curso=id_curso,
            )
            session.add(resena)
            session.commit()
            session.refresh(resena)
            return resena
        finally:
            session.close()

    def listar(self) -> list[Resena]:
        session = get_session()
        try:
            return session.query(Resena).all()
        finally:
            session.close()

    def obtener_por_curso(self, id_curso: UUID) -> list[Resena]:
        """Devuelve todas las reseñas pertenecientes a un curso específico."""
        session = get_session()
        try:
            return session.query(Resena).filter_by(id_curso=id_curso).all()
        finally:
            session.close()

    def obtener_por_usuario(self, id_usuario: UUID) -> list[Resena]:
        """Devuelve todas las reseñas escritas por un usuario."""
        session = get_session()
        try:
            return session.query(Resena).filter_by(id_usuario=id_usuario).all()
        finally:
            session.close()

    def obtener_por_usuario_curso(
        self, id_usuario: UUID, id_curso: UUID
    ) -> Resena | None:
        session = get_session()
        try:
            return (
                session.query(Resena)
                .filter_by(id_usuario=id_usuario, id_curso=id_curso)
                .first()
            )
        finally:
            session.close()

    def actualizar(
        self, identificador: UUID, calificacion: int, comentario: str | None
    ) -> Resena | None:
        session = get_session()
        try:
            resena = session.get(Resena, identificador)
            if resena is None:
                return None
            resena.calificacion = calificacion
            resena.comentario = comentario
            session.commit()
            session.refresh(resena)
            return resena
        finally:
            session.close()

    def promedio_calificacion_curso(self, id_curso: UUID) -> float:
        """Calcula el promedio de calificación usando funciones agregadas de la base de datos."""
        session = get_session()
        try:
            # func.avg calcula directamente el promedio en la Base de Datos (Neon DB)
            resultado = (
                session.query(func.avg(Resena.calificacion))
                .filter_by(id_curso=id_curso)
                .scalar()
            )
            if resultado is None:
                return 0.0
            return round(float(resultado), 2)
        finally:
            session.close()
