from uuid import UUID
from database.connection import get_session
from src.models.usuario import Usuario  # Ajusta la importación según la ubicación de tus modelos


class UsuarioCRUD:
    def crear(
        self,
        primer_nombre: str,
        primer_apellido: str,
        nombre_usuario: str,
        correo: str,
        clave: str,
        segundo_nombre: str = "",
        segundo_apellido: str = "",
        area: str = "",
        id_rol: UUID | None = None,
    ) -> Usuario | None:
        session = get_session()
        try:
            # Validar si ya existe el nombre_usuario o correo
            existe = (
                session.query(Usuario)
                .filter(
                    (Usuario.nombre_usuario == nombre_usuario) | (Usuario.correo == correo)
                )
                .first()
            )
            if existe:
                return None

            usuario = Usuario(
                primer_nombre=primer_nombre,
                segundo_nombre=segundo_nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                nombre_usuario=nombre_usuario,
                correo=correo,
                clave=clave,
                area=area,
                id_rol=id_rol,
            )
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario
        finally:
            session.close()

    def listar(self) -> list[Usuario]:
        session = get_session()
        try:
            return session.query(Usuario).all()
        finally:
            session.close()

    def obtener_por_id(self, id_usuario: UUID) -> Usuario | None:
        session = get_session()
        try:
            return session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        finally:
            session.close()

    def buscar_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        session = get_session()
        try:
            nombre_clean = nombre_usuario.strip()
            # ilike hace la búsqueda insensible a mayúsculas/minúsculas en PostgreSQL
            return (
                session.query(Usuario)
                .filter(Usuario.nombre_usuario.ilike(nombre_clean))
                .first()
            )
        finally:
            session.close()

    def autenticar(self, nombre_usuario: str, clave: str) -> Usuario | None:
        session = get_session()
        try:
            nombre_clean = nombre_usuario.strip()
            return (
                session.query(Usuario)
                .filter(
                    Usuario.nombre_usuario.ilike(nombre_clean),
                    Usuario.clave == clave,
                )
                .first()
            )
        finally:
            session.close()