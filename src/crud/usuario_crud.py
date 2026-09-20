from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.usuario import Usuario


def _buscar_por_id(session, id_usuario: UUID) -> Usuario | None:
    return session.query(Usuario).filter_by(id_usuario=id_usuario).first()


def _buscar_por_nombre(session, nombre_usuario: str) -> Usuario | None:
    nombre = nombre_usuario.strip().lower()
    return (
        session.query(Usuario)
        .filter(func.lower(Usuario.nombre_usuario) == nombre)
        .first()
    )


def _buscar_por_correo(session, correo: str) -> Usuario | None:
    correo_clean = correo.strip().lower()
    return (
        session.query(Usuario)
        .filter(func.lower(Usuario.correo) == correo_clean)
        .first()
    )


def crear(
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
        if _buscar_por_nombre(session, nombre_usuario) or _buscar_por_correo(session, correo):
            return None

        usuario = Usuario(
            primer_nombre=primer_nombre.strip(),
            segundo_nombre=(segundo_nombre or "").strip(),
            primer_apellido=primer_apellido.strip(),
            segundo_apellido=(segundo_apellido or "").strip(),
            nombre_usuario=nombre_usuario.strip(),
            correo=correo.strip().lower(),
            clave=clave,
            area=(area or "").strip(),
            id_rol=id_rol,
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_usuario: UUID) -> bool:
    session = get_session()
    try:
        usuario = _buscar_por_id(session, id_usuario)
        if usuario is None:
            return False
        session.delete(usuario)
        session.commit()
        return True
    finally:
        session.close()


def actualizar(id_usuario: UUID, **kwargs: Any) -> Usuario | None:
    session = get_session()
    try:
        usuario = _buscar_por_id(session, id_usuario)
        if usuario is None:
            return None

        # Validaciones de duplicados para nombre_usuario o correo
        nombre_usuario = kwargs.get("nombre_usuario")
        if nombre_usuario:
            existente = _buscar_por_nombre(session, nombre_usuario)
            if existente is not None and existente.id_usuario != id_usuario:
                return None

        correo = kwargs.get("correo")
        if correo:
            existente_correo = _buscar_por_correo(session, correo)
            if existente_correo is not None and existente_correo.id_usuario != id_usuario:
                return None

        # Asignar los valores recibidos
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    setattr(usuario, key, value.strip())
                else:
                    setattr(usuario, key, value)

        session.commit()
        session.refresh(usuario)
        return usuario
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(nombre_usuario: str, clave: str) -> Usuario | None:
    session = get_session()
    try:
        usuario = _buscar_por_nombre(session, nombre_usuario)
        if usuario is None or usuario.clave != clave:
            return None
        return usuario
    finally:
        session.close()


def obtener_por_id(id_usuario: UUID) -> Usuario | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_usuario)
    finally:
        session.close()


def listar() -> list[Usuario]:
    session = get_session()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()