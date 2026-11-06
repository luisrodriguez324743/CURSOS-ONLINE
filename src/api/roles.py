from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.crud.rol_crud import RolCRUD
from src.api.schemas import (
    RolCreate,
    RolRead,
    RolPost,
    RolList,
    RolUpdate,
    RolPut,
)

roles_router = APIRouter(prefix="/roles", tags=["roles"])
rol_crud = RolCRUD()


@roles_router.get("/", response_model=RolList)
def listar_roles() -> RolList:
    roles = rol_crud.listar()
    if not roles:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron roles"
        )
    return {
        "data": roles,
        "status": HTTPStatus.OK.value,
        "message": "Roles encontrados",
    }


@roles_router.get("/{id_rol}", response_model=RolRead)
def obtener_rol(id_rol: UUID):
    rol = rol_crud.obtener_por_id(id_rol)
    if rol is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Rol no encontrado"
        )
    return rol


@roles_router.post("/", response_model=RolPost, status_code=HTTPStatus.CREATED.value)
def crear_rol(datos: RolCreate):
    rol = rol_crud.crear(**datos.model_dump())
    if rol is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Ya existe un rol con ese nombre",
        )

    return {
        "data": rol,
        "status": HTTPStatus.CREATED.value,
        "message": f"Rol {rol.nombre_rol} creado exitosamente",
    }


@roles_router.put("/{id_rol}", response_model=RolPut)
def actualizar_rol(id_rol: UUID, datos: RolUpdate):
    rol_existente = rol_crud.obtener_por_id(id_rol)
    if rol_existente is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Rol no encontrado"
        )

    rol_con_nombre = rol_crud.buscar_por_nombre(datos.nombre_rol)
    if rol_con_nombre is not None and rol_con_nombre.id_rol != id_rol:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Ya existe un rol con ese nombre",
        )

    try:
        rol = rol_crud.actualizar(
            id_rol, datos.nombre_rol, datos.descripcion
        )
    except IntegrityError as error:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Ya existe un rol con ese nombre",
        ) from error

    if rol is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Rol no encontrado"
        )
    return {
        "data": rol,
        "status": HTTPStatus.OK.value,
        "message": f"Rol {rol.nombre_rol} actualizado exitosamente",
    }


@roles_router.delete("/{id_rol}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_rol(id_rol: UUID) -> None:
    try:
        eliminado = rol_crud.eliminar(id_rol)
    except IntegrityError as error:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se puede eliminar el rol porque está asignado a usuarios",
        ) from error
    if not eliminado:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Rol no encontrado"
        )