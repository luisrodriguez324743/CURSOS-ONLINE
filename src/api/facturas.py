from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    FacturaCreate,
    FacturaList,
    FacturaPost,
    FacturaPut,
    FacturaRead,
    FacturaUpdate,
)
from src.crud.factura_crud import FacturaCRUD
from src.crud.curso_crud import CursoCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud import usuario_crud
from src.entities.factura import Factura

facturas_router = APIRouter(prefix="/facturas", tags=["facturas"])
factura_crud = FacturaCRUD()
curso_crud = CursoCRUD()
inscripcion_crud = InscripcionCRUD()


@facturas_router.get("/", response_model=FacturaList)
def listar_facturas() -> dict[str, Any]:
    facturas = factura_crud.listar()
    if not facturas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron facturas",
        )
    return {
        "data": facturas,
        "status": HTTPStatus.OK.value,
        "message": "Facturas encontradas",
    }


@facturas_router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(id_factura: UUID) -> Factura:
    factura = factura_crud.obtener(id_factura)
    if factura is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Factura no encontrada"
        )
    return factura


@facturas_router.post(
    "/", response_model=FacturaPost, status_code=HTTPStatus.CREATED.value
)
def crear_factura(datos: FacturaCreate) -> dict[str, Any]:
    valores = datos.model_dump(exclude_none=True)
    if usuario_crud.obtener_por_id(datos.id_usuario) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )

    curso = curso_crud.obtener(datos.id_curso)
    if curso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )

    inscripcion = inscripcion_crud.obtener(datos.id_inscripcion)
    if inscripcion is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Inscripción no encontrada",
        )
    if (
        inscripcion.id_usuario != datos.id_usuario
        or inscripcion.id_curso != datos.id_curso
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="La inscripción no corresponde al usuario y curso indicados",
        )

    valores["total"] = curso.precio
    valores["numero_factura"] = ""

    try:
        factura = factura_crud.crear(Factura(**valores))
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)) from error
    return {
        "data": factura,
        "status": HTTPStatus.CREATED.value,
        "message": f"Factura {factura.numero_factura} creada exitosamente",
    }


@facturas_router.put("/{id_factura}", response_model=FacturaPut)
def actualizar_factura(id_factura: UUID, datos: FacturaUpdate) -> dict[str, Any]:
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    try:
        factura = factura_crud.actualizar(id_factura, cambios)
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)) from error
    if factura is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Factura no encontrada"
        )
    return {
        "data": factura,
        "status": HTTPStatus.OK.value,
        "message": f"Factura {factura.numero_factura} actualizada exitosamente",
    }


@facturas_router.delete("/{id_factura}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_factura(id_factura: UUID) -> None:
    if not factura_crud.eliminar(id_factura):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Factura no encontrada"
        )