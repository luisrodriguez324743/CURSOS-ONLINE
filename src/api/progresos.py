from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import ProgresoEstadoRead, ProgresoEstadoUpdate
from src.crud.progreso_crud import ProgresoCRUD

progresos_router = APIRouter(prefix="/progresos", tags=["progresos"])
progreso_crud = ProgresoCRUD()


@progresos_router.patch(
    "/usuario/{id_usuario}/curso/{id_curso}/estado",
    response_model=ProgresoEstadoRead,
)
def actualizar_estado_progreso(
    id_usuario: UUID, id_curso: UUID, datos: ProgresoEstadoUpdate
) -> dict[str, Any]:
    progreso = next(
        (
            registro
            for registro in progreso_crud.listar()
            if registro.id_usuario == id_usuario
            and registro.id_curso == id_curso
            and registro.id_leccion is None
        ),
        None,
    )
    if progreso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontró el progreso del usuario en este curso",
        )
    if datos.estado == "Completado" and progreso.porcentaje < 100:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El curso solo puede marcarse como completado al llegar al 100%",
        )

    progreso = progreso_crud.actualizar(
        progreso.id_progreso, {"estado": datos.estado}
    )
    if progreso is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontró el progreso del usuario en este curso",
        )
    return {
        "id_curso": id_curso,
        "id_usuario": id_usuario,
        "estado": progreso.estado,
        "porcentaje": progreso.porcentaje,
    }