from typing import Any, Dict, List
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.crud.resena_crud import ResenaCRUD
from src.api.schemas import (
    ResenaCreate,
    ResenaUpdate,
    ResenaRead,
    ResenaPost,
    ResenaList,
    ResenaPut,
    PromedioResena,
)

resenas_router = APIRouter(prefix="/resenas", tags=["resenas"])
resena_crud = ResenaCRUD()


@resenas_router.get("/", response_model=ResenaList)
def listar_resenas() -> ResenaList:
    resenas = resena_crud.listar()
    if not resenas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron reseñas"
        )
    return {
        "data": resenas,
        "status": HTTPStatus.OK.value,
        "message": "Reseñas encontradas",
    }


@resenas_router.get("/curso/{id_curso}", response_model=List[ResenaRead])
def obtener_por_curso(id_curso: UUID):
    return resena_crud.obtener_por_curso(id_curso)


@resenas_router.get("/curso/{id_curso}/promedio", response_model=PromedioResena)
def obtener_promedio_curso(id_curso: UUID):
    promedio = resena_crud.promedio_calificacion_curso(id_curso)
    return {"id_curso": id_curso, "promedio": promedio}


@resenas_router.get("/usuario/{id_usuario}", response_model=List[ResenaRead])
def obtener_por_usuario(id_usuario: UUID):
    return resena_crud.obtener_por_usuario(id_usuario)


@resenas_router.get("/usuario/{id_usuario}/curso/{id_curso}", response_model=ResenaRead)
def obtener_por_usuario_curso(id_usuario: UUID, id_curso: UUID):
    resena = resena_crud.obtener_por_usuario_curso(id_usuario, id_curso)
    if resena is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Reseña no encontrada"
        )
    return resena


@resenas_router.post("/", response_model=ResenaPost, status_code=HTTPStatus.CREATED.value)
def crear_resena(datos: ResenaCreate):
    resena = resena_crud.crear(**datos.model_dump())
    return {
        "data": resena,
        "status": HTTPStatus.CREATED.value,
        "message": "Reseña registrada exitosamente",
    }


@resenas_router.put("/{id_resena}", response_model=ResenaPut)
def actualizar_resena(id_resena: UUID, datos: ResenaUpdate):
    resena = resena_crud.actualizar(
        identificador=id_resena,
        calificacion=datos.calificacion,
        comentario=datos.comentario,
    )
    if resena is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Reseña no encontrada"
        )

    return {
        "data": resena,
        "status": HTTPStatus.OK.value,
        "message": "Reseña actualizada exitosamente",
    }