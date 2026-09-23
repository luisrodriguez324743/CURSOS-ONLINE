from typing import Any, Dict
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.crud.rol_crud import RolCRUD
from src.api.schemas import (
    RolCreate,
    RolRead,
    RolPost,
)

roles_router = APIRouter(prefix="/roles", tags=["roles"])
rol_crud = RolCRUD()


@roles_router.get("/", response_model=Dict[str, Any])
def listar_roles() -> Dict[str, Any]:
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