from typing import Any, Dict, List
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    CursoCreate,
    CursoList,
    CursoPost,
    CursoPut,
    CursoRead,
    CursoUpdate,
)
from src.crud import usuario_crud
from src.crud.curso_crud import CursoCRUD
from src.entities.curso import Curso

cursos_router = APIRouter(prefix="/cursos", tags=["cursos"])
curso_crud = CursoCRUD()


@cursos_router.get("/", response_model=CursoList)
def listar_cursos() -> dict[str, Any]:
    cursos = curso_crud.listar()
    if not cursos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron cursos"
        )
    return {
        "data": cursos,
        "status": HTTPStatus.OK.value,
        "message": "Cursos encontrados",
    }


@cursos_router.get("/{id_curso}", response_model=CursoRead)
def obtener_curso(id_curso: UUID) -> Curso:
    curso = curso_crud.obtener(id_curso)
    if curso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )
    return curso


@cursos_router.post("/", response_model=CursoPost, status_code=HTTPStatus.CREATED.value)
def crear_curso(datos: CursoCreate) -> dict[str, Any]:
    if (
        datos.id_profesor is not None
        and usuario_crud.obtener_por_id(datos.id_profesor) is None
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Profesor no encontrado"
        )

    curso = curso_crud.crear(Curso(**datos.model_dump()))
    return {
        "data": curso,
        "status": HTTPStatus.CREATED.value,
        "message": f"Curso {curso.nombre} creado exitosamente",
    }


@cursos_router.put("/{id_curso}", response_model=CursoPut)
def actualizar_curso(id_curso: UUID, datos: CursoUpdate) -> dict[str, Any]:
    cambios = {
        nombre: valor
        for nombre, valor in datos.model_dump(exclude_unset=True).items()
        if valor is not None or nombre == "id_profesor"
    }
    if "id_profesor" in cambios and cambios["id_profesor"] is not None:
        if usuario_crud.obtener_por_id(cambios["id_profesor"]) is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Profesor no encontrado"
            )

    curso = curso_crud.actualizar(id_curso, cambios)
    if curso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )
    return {
        "data": curso,
        "status": HTTPStatus.OK.value,
        "message": f"Curso {curso.nombre} actualizado exitosamente",
    }


@cursos_router.delete("/{id_curso}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_curso(id_curso: UUID) -> None:
    if not curso_crud.eliminar(id_curso):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )
