from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import PagoCreate, PagoList, PagoPost, PagoPut, PagoRead, PagoUpdate
from src.crud import usuario_crud
from src.crud.curso_crud import CursoCRUD
from src.crud.factura_crud import FacturaCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud.pago_crud import PagoCRUD
from src.entities.factura import Factura
from src.entities.pago import Pago

pagos_router = APIRouter(prefix="/pagos", tags=["pagos"])
pago_crud = PagoCRUD()
curso_crud = CursoCRUD()
inscripcion_crud = InscripcionCRUD()
factura_crud = FacturaCRUD()


@pagos_router.get("/", response_model=PagoList)
def listar_pagos() -> dict[str, Any]:
    pagos = pago_crud.listar()
    if not pagos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron pagos"
        )
    return {"data": pagos, "status": HTTPStatus.OK.value, "message": "Pagos encontrados"}


@pagos_router.get("/{id_pago}", response_model=PagoRead)
def obtener_pago(id_pago: UUID) -> Pago:
    pago = pago_crud.obtener(id_pago)
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Pago no encontrado"
        )
    return pago


@pagos_router.post("/", response_model=PagoPost, status_code=HTTPStatus.CREATED.value)
def crear_pago(datos: PagoCreate) -> dict[str, Any]:
    if usuario_crud.obtener_por_id(datos.id_usuario) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )

    curso = curso_crud.obtener(datos.id_curso)
    if curso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
        )

    inscripcion = next(
        (
            registro
            for registro in inscripcion_crud.listar()
            if registro.id_usuario == datos.id_usuario
            and registro.id_curso == datos.id_curso
        ),
        None,
    )
    if inscripcion is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El usuario debe estar inscrito en este curso antes de realizar el pago",
        )

    pago_confirmado = any(
        registro.id_usuario == datos.id_usuario
        and registro.id_curso == datos.id_curso
        and registro.estado == "pagado"
        for registro in pago_crud.listar()
    )
    factura_pagada = any(
        registro.id_usuario == datos.id_usuario
        and registro.id_curso == datos.id_curso
        and registro.estado == "pagada"
        for registro in factura_crud.listar()
    )
    if pago_confirmado or factura_pagada:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El usuario ya tiene el curso pagado",
        )

    pago = Pago(
        monto=curso.precio,
        metodo_pago=datos.metodo_pago,
        estado=datos.estado,
        id_usuario=datos.id_usuario,
        id_curso=datos.id_curso,
    )
    try:
        if pago.estado == "pagado":
            factura = Factura(
                numero_factura="",
                total=curso.precio,
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=datos.id_usuario,
                id_curso=datos.id_curso,
                metodo_pago=datos.metodo_pago,
                estado="pagada",
            )
            pago, factura = pago_crud.crear_con_factura(pago, factura)
            mensaje = f"Pago registrado y factura {factura.numero_factura} generada exitosamente"
        else:
            pago = pago_crud.crear(pago)
            mensaje = "Pago registrado; la factura se generará al confirmarlo"
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)) from error
    return {
        "data": pago,
        "status": HTTPStatus.CREATED.value,
        "message": mensaje,
    }


@pagos_router.put("/{id_pago}", response_model=PagoPut)
def actualizar_pago(id_pago: UUID, datos: PagoUpdate) -> dict[str, Any]:
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    pago_actual = pago_crud.obtener(id_pago)
    if pago_actual is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Pago no encontrado"
        )
    estado_final = cambios.get("estado", pago_actual.estado)
    confirmar_pago = estado_final == "pagado" and pago_actual.id_factura is None
    curso_id = cambios.get("id_curso", pago_actual.id_curso)
    if curso_id is not None:
        curso = curso_crud.obtener(curso_id)
        if curso is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Curso no encontrado"
            )
        cambios["monto"] = curso.precio
    try:
        pago = pago_crud.actualizar(id_pago, cambios)
        if confirmar_pago:
            if pago.id_usuario is None or pago.id_curso is None:
                raise ValueError("El pago debe tener usuario y curso para generar factura.")
            curso = curso_crud.obtener(pago.id_curso)
            inscripcion = next(
                (
                    registro
                    for registro in inscripcion_crud.listar()
                    if registro.id_usuario == pago.id_usuario
                    and registro.id_curso == pago.id_curso
                ),
                None,
            )
            if curso is None or inscripcion is None:
                raise ValueError("El pago debe tener un curso y una inscripción relacionados.")
            factura = Factura(
                numero_factura="",
                total=curso.precio,
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=pago.id_usuario,
                id_curso=pago.id_curso,
                metodo_pago=pago.metodo_pago,
                estado="pagada",
            )
            factura = factura_crud.crear(factura)
            pago = pago_crud.actualizar(id_pago, {"id_factura": factura.id_factura})
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=str(error)) from error
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Pago no encontrado"
        )
    return {
        "data": pago,
        "status": HTTPStatus.OK.value,
        "message": "Pago actualizado y factura generada" if confirmar_pago else "Pago actualizado exitosamente",
    }


@pagos_router.delete("/{id_pago}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_pago(id_pago: UUID) -> None:
    if not pago_crud.eliminar(id_pago):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Pago no encontrado"
        )