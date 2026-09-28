from typing import Any, Dict, List
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ModuloCreate,
    ModuloList,
    ModuloPost,
    ModuloPut,
    ModuloRead,
    ModuloUpdate,
)
from src.crud.curso_crud import CursoCRUD
from src.crud.modulo_crud import ModuloCRUD
from src.entities.modulo import Modulo

modulos_router = APIRouter(prefix="/modulos", tags=["modulos"])
modulo_crud = ModuloCRUD()
curso_crud = CursoCRUD()


@modulos_router.get("/", response_model=ModuloList)
def listar_modulos() -> dict[str, Any]:
    modulos = modulo_crud.listar()
    if not modulos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron módulos"
        )
    return {
        "data": modulos,
        "status": HTTPStatus.OK.value,
        "message": "Módulos encontrados",
    }


@modulos_router.get("/{id_modulo}", response_model=ModuloRead)
def obtener_modulo(id_modulo: UUID) -> Modulo:
    modulo = modulo_crud.obtener(id_modulo)
    if modulo is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Módulo no encontrado"
        )
    return modulo


@modulos_router.post(
    "/", response_model=ModuloPost, status_code=HTTPStatus.CREATED.value
)
def crear_modulo(datos: ModuloCreate) -> dict[str, Any]:
    if curso_crud.obtener(datos.id_curso) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )
    modulo = modulo_crud.crear(Modulo(**datos.model_dump()))
    return {
        "data": modulo,
        "status": HTTPStatus.CREATED.value,
        "message": f"Módulo {modulo.nombre} creado exitosamente",
    }


@modulos_router.put("/{id_modulo}", response_model=ModuloPut)
def actualizar_modulo(id_modulo: UUID, datos: ModuloUpdate) -> dict[str, Any]:
    cambios = {
        nombre: valor
        for nombre, valor in datos.model_dump(exclude_unset=True).items()
        if valor is not None
    }
    if "id_curso" in cambios and curso_crud.obtener(cambios["id_curso"]) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )

    modulo = modulo_crud.actualizar(id_modulo, cambios)
    if modulo is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Módulo no encontrado"
        )
    return {
        "data": modulo,
        "status": HTTPStatus.OK.value,
        "message": f"Módulo {modulo.nombre} actualizado exitosamente",
    }


@modulos_router.delete("/{id_modulo}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_modulo(id_modulo: UUID) -> None:
    if not modulo_crud.eliminar(id_modulo):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Módulo no encontrado"
        )
