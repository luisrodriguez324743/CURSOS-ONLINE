from uuid import UUID
from src.database.connection import get_session
from src.entities.rol import Rol


class RolCRUD:
    def crear(self, nombre_rol: str, descripcion: str | None = None) -> Rol | None:
        session = get_session()
        try:
            if session.query(Rol).filter_by(nombre_rol=nombre_rol).first():
                return None

            rol = Rol(nombre_rol=nombre_rol, descripcion=descripcion)
            session.add(rol)
            session.commit()
            session.refresh(rol)
            return rol
        finally:
            session.close()

    def listar(self) -> list[Rol]:
        session = get_session()
        try:
            return session.query(Rol).all()
        finally:
            session.close()

    def obtener_por_id(self, id_rol: UUID) -> Rol | None:
        session = get_session()
        try:
            return session.query(Rol).filter_by(id_rol=id_rol).first()
        finally:
            session.close()

    def buscar_por_nombre(self, nombre: str) -> Rol | None:
        """Encuentra un rol por su nombre ignorando mayúsculas/minúsculas."""
        session = get_session()
        try:
            nombre_clean = nombre.strip()
            return (
                session.query(Rol)
                .filter(Rol.nombre_rol.ilike(nombre_clean))
                .first()
            )
        finally:
            session.close()