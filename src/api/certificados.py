from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    CertificadoCreate,
    CertificadoElegibilidad,
    CertificadoList,
    CertificadoPost,
    CertificadoPut,
    CertificadoRead,
    CertificadoUpdate,
)
from src.crud.certificado_crud import CertificadoCRUD
from src.crud.factura_crud import FacturaCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud.pago_crud import PagoCRUD
from src.crud.progreso_crud import ProgresoCRUD
from src.entities.certificado import Certificado

certificados_router = APIRouter(prefix="/certificados", tags=["certificados"])
certificado_crud = CertificadoCRUD()
factura_crud = FacturaCRUD()
inscripcion_crud = InscripcionCRUD()
pago_crud = PagoCRUD()
progreso_crud = ProgresoCRUD()


@certificados_router.get("/", response_model=CertificadoList)
def listar_certificados() -> dict[str, Any]:
    certificados = certificado_crud.listar()
    if not certificados:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron certificados",
        )
    return {
        "data": certificados,
        "status": HTTPStatus.OK.value,
        "message": "Certificados encontrados",
    }


@certificados_router.get(
    "/revisar/usuario/{id_usuario}/curso/{id_curso}",
    response_model=CertificadoElegibilidad,
)
def revisar_elegibilidad_certificado(
    id_usuario: UUID, id_curso: UUID
) -> dict[str, Any]:
    certificado = certificado_crud.obtener_por_usuario_curso(id_usuario, id_curso)
    if certificado is not None:
        puede_emitirse = False
        mensaje = "Ya existe un certificado para este usuario y curso."
    else:
        puede_emitirse, mensaje = certificado_crud.puede_emitirse(
            pagos=pago_crud.listar(),
            facturas=factura_crud.listar(),
            progresos=progreso_crud.listar(),
            inscripciones=inscripcion_crud.listar(),
            id_usuario=id_usuario,
            id_curso=id_curso,
        )
    return {
        "id_usuario": id_usuario,
        "id_curso": id_curso,
        "puede_emitirse": puede_emitirse,
        "mensaje": mensaje,
        "certificado": certificado,
    }


@certificados_router.get(
    "/usuario/{id_usuario}/curso/{id_curso}", response_model=CertificadoRead
)
def obtener_certificado_usuario_curso(id_usuario: UUID, id_curso: UUID) -> Certificado:
    certificado = certificado_crud.obtener_por_usuario_curso(id_usuario, id_curso)
    if certificado is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Certificado no encontrado"
        )
    return certificado


@certificados_router.get("/{id_certificado}", response_model=CertificadoRead)
def obtener_certificado(id_certificado: UUID) -> Certificado:
    certificado = certificado_crud.obtener(id_certificado)
    if certificado is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Certificado no encontrado"
        )
    return certificado


@certificados_router.post(
    "/", response_model=CertificadoPost, status_code=HTTPStatus.CREATED.value
)
def crear_certificado(datos: CertificadoCreate) -> dict[str, Any]:
    if certificado_crud.obtener_por_usuario_curso(datos.id_usuario, datos.id_curso):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Ya existe un certificado para este usuario y curso.",
        )

    puede_emitirse, mensaje = certificado_crud.puede_emitirse(
        pagos=pago_crud.listar(),
        facturas=factura_crud.listar(),
        progresos=progreso_crud.listar(),
        inscripciones=inscripcion_crud.listar(),
        id_usuario=datos.id_usuario,
        id_curso=datos.id_curso,
    )
    if not puede_emitirse:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=mensaje,
        )

    try:
        certificado = certificado_crud.crear(
            Certificado(**datos.model_dump(exclude_none=True))
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value, detail=str(error)
        ) from error
    return {
        "data": certificado,
        "status": HTTPStatus.CREATED.value,
        "message": f"Certificado {certificado.codigo} emitido exitosamente",
    }


@certificados_router.put("/{id_certificado}", response_model=CertificadoPut)
def actualizar_certificado(
    id_certificado: UUID, datos: CertificadoUpdate
) -> dict[str, Any]:
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    certificado = certificado_crud.actualizar(id_certificado, cambios)
    if certificado is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Certificado no encontrado"
        )
    return {
        "data": certificado,
        "status": HTTPStatus.OK.value,
        "message": f"Certificado {certificado.codigo} actualizado exitosamente",
    }


@certificados_router.delete(
    "/{id_certificado}", status_code=HTTPStatus.NO_CONTENT.value
)
def eliminar_certificado(id_certificado: UUID) -> None:
    if not certificado_crud.eliminar(id_certificado):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Certificado no encontrado"
        )
