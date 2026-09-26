from typing import Any, Dict, List
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    LeccionCreate,
    LeccionList,
    LeccionPost,
    LeccionPut,
    LeccionRead,
    LeccionUpdate,
)
from src.crud.leccion_crud import LeccionCRUD
from src.crud.modulo_crud import ModuloCRUD
from src.entities.leccion import Leccion

lecciones_router = APIRouter(prefix="/lecciones", tags=["lecciones"])
leccion_crud = LeccionCRUD()
modulo_crud = ModuloCRUD()


@lecciones_router.get("/", response_model=LeccionList)
def listar_lecciones() -> dict[str, Any]:
    lecciones = leccion_crud.listar()
    if not lecciones:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron lecciones"
        )
    return {
        "data": lecciones,
        "status": HTTPStatus.OK.value,
        "message": "Lecciones encontradas",
    }


@lecciones_router.get("/{id_leccion}", response_model=LeccionRead)
def obtener_leccion(id_leccion: UUID) -> Leccion:
    leccion = leccion_crud.obtener(id_leccion)
    if leccion is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Lección no encontrada"
        )
    return leccion


@lecciones_router.post(
    "/", response_model=LeccionPost, status_code=HTTPStatus.CREATED.value
)
def crear_leccion(datos: LeccionCreate) -> dict[str, Any]:
    if modulo_crud.obtener(datos.id_modulo) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Módulo no encontrado"
        )
    leccion = leccion_crud.crear(Leccion(**datos.model_dump()))
    return {
        "data": leccion,
        "status": HTTPStatus.CREATED.value,
        "message": f"Lección {leccion.nombre} creada exitosamente",
    }


@lecciones_router.put("/{id_leccion}", response_model=LeccionPut)
def actualizar_leccion(id_leccion: UUID, datos: LeccionUpdate) -> dict[str, Any]:
    cambios = {
        nombre: valor
        for nombre, valor in datos.model_dump(exclude_unset=True).items()
        if valor is not None
    }
    if "id_modulo" in cambios and modulo_crud.obtener(cambios["id_modulo"]) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Módulo no encontrado"
        )

    leccion = leccion_crud.actualizar(id_leccion, cambios)
    if leccion is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Lección no encontrada"
        )
    return {
        "data": leccion,
        "status": HTTPStatus.OK.value,
        "message": f"Lección {leccion.nombre} actualizada exitosamente",
    }


@lecciones_router.delete("/{id_leccion}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_leccion(id_leccion: UUID) -> None:
    if not leccion_crud.eliminar(id_leccion):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Lección no encontrada"
        )
