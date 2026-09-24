from typing import Any
from uuid import UUID
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from src.crud import usuario_crud
from http import HTTPStatus

from src.api.schemas import (
    UsuarioCreate, 
    UsuarioLogin, 
    UsuarioRead, 
    UsuarioUpdate, 
    UsuarioList,
    usuarioPost, 
    usuarioPut)

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuarios_router.get("/", response_model=UsuarioList)
def get_usuarios() -> UsuarioList:
    usuarios = usuario_crud.listar()
    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron usuarios"
        )
     
    return {
        "data": usuarios,
        "status": HTTPStatus.OK.value,
        "message": "Usuarios encontrados",
    }


@usuarios_router.post("/login", response_model=UsuarioRead)
def iniciar_sesion(datos: UsuarioLogin):
    usuario = usuario_crud.obtener(datos.nombre_usuario, datos.clave)
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Nombre de usuario o clave incorrectos",
        )
    return usuario


@usuarios_router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID):
    usuario = usuario_crud.obtener_por_id(id_usuario)
    if usuario is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado")
    return usuario


@usuarios_router.post("/", response_model=usuarioPost, status_code=HTTPStatus.CREATED.value)
def crear_usuario(datos: UsuarioCreate):
    usuario = usuario_crud.crear(**datos.model_dump())

    if usuario is None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="El nombre de usuario o correo ya existe")

    return{
        "data": usuario,
        "status": HTTPStatus.CREATED.value,
        "message": f"Usuario {usuario.nombre_usuario} creado exitosamente",
    }

    
@usuarios_router.put("/{id_usuario}", response_model=usuarioPut)
def actualizar_usuario(id_usuario: UUID, datos: UsuarioUpdate):
    datos = usuario_crud.obtener_por_id(id_usuario)
    if usuario_crud.obtener_por_id(id_usuario) is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado")
    
    usuario = usuario_crud.actualizar(
        id_usuario,
        **datos.model_dump(exclude_unset=True),
    )
    if usuario is None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="El nombre de usuario o correo ya existe",)

    return{
        "data": usuario,
        "status": HTTPStatus.OK.value,
        "message": f"Usuario {usuario.nombre_usuario} actualizado exitosamente",
    }


@usuarios_router.delete("/{id_usuario}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_usuario(id_usuario: UUID):
    if not usuario_crud.eliminar(id_usuario):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado")