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
from src.crud.pago_crud import PagoCRUD
from src.crud import usuario_crud
from src.entities.factura import Factura

facturas_router = APIRouter(prefix="/facturas", tags=["facturas"])
factura_crud = FacturaCRUD()
curso_crud = CursoCRUD()
inscripcion_crud = InscripcionCRUD()
pago_crud = PagoCRUD()


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
    valores.pop("id_pago", None)
    if usuario_crud.obtener_por_id(datos.id_usuario) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )

    curso = curso_crud.obtener(datos.id_curso)
    if curso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )

    pago = pago_crud.obtener(datos.id_pago)
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Pago no encontrado"
        )
    if pago.estado != "pagado":
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Solo los pagos confirmados pueden generar una factura",
        )
    if pago.id_usuario != datos.id_usuario or pago.id_curso != datos.id_curso:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El pago no corresponde al usuario y curso indicados",
        )
    if pago.id_factura is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El pago ya tiene una factura asociada",
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
        pago_crud.actualizar(datos.id_pago, {"id_factura": factura.id_factura})
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)
        ) from error
    return {
        "data": factura,
        "status": HTTPStatus.CREATED.value,
        "message": f"Factura {factura.numero_factura} creada exitosamente",
    }


@facturas_router.put("/{id_factura}", response_model=FacturaPut)
def actualizar_factura(id_factura: UUID, datos: FacturaUpdate) -> dict[str, Any]:
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    factura_actual = factura_crud.obtener(id_factura)
    if factura_actual is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Factura no encontrada"
        )
    usuario_id = cambios.get("id_usuario", factura_actual.id_usuario)
    curso_id = cambios.get("id_curso", factura_actual.id_curso)
    inscripcion_id = cambios.get("id_inscripcion", factura_actual.id_inscripcion)
    pago_vinculado = next(
        (pago for pago in pago_crud.listar() if pago.id_factura == id_factura),
        None,
    )
    relaciones_cambiadas = (
        usuario_id != factura_actual.id_usuario
        or curso_id != factura_actual.id_curso
        or inscripcion_id != factura_actual.id_inscripcion
    )
    if pago_vinculado is not None and relaciones_cambiadas:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se pueden cambiar las relaciones de una factura vinculada a un pago",
        )
    if relaciones_cambiadas:
        if usuario_id is None or curso_id is None or inscripcion_id is None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT.value,
                detail="La factura necesita usuario, curso e inscripción relacionados",
            )
        if usuario_crud.obtener_por_id(usuario_id) is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
            )
        if curso_crud.obtener(curso_id) is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
            )
        inscripcion = inscripcion_crud.obtener(inscripcion_id)
        if inscripcion is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value,
                detail="Inscripción no encontrada",
            )
        if inscripcion.id_usuario != usuario_id or inscripcion.id_curso != curso_id:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT.value,
                detail="La inscripción no corresponde al usuario y curso indicados",
            )
    try:
        factura = factura_crud.actualizar(id_factura, cambios)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)
        ) from error
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
