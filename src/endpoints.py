from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.crud.evaluacion_crud import EvaluacionCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud.progreso_crud import ProgresoCRUD
from src.entities.evaluacion import Evaluacion
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso

# ROUTERS


router_inscripciones = APIRouter(
    prefix="/inscripciones",
    tags=["Inscripciones"],
)

router_progresos = APIRouter(
    prefix="/progresos",
    tags=["Progresos"],
)

router_evaluaciones = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluaciones"],
)

# SCHEMAS DE INSCRIPCIÓN


class InscripcionCreate(BaseModel):
    estado: str = "activa"
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None


class InscripcionUpdate(BaseModel):
    estado: Optional[str] = None
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None


class InscripcionResponse(BaseModel):
    id_inscripcion: UUID
    fecha_inscripcion: datetime
    estado: str
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)

# ENDPOINTS DE INSCRIPCIÓN


@router_inscripciones.get(
    "/",
    response_model=list[InscripcionResponse],
    status_code=status.HTTP_200_OK,
)
def listar_inscripciones() -> list[Inscripcion]:
    crud = InscripcionCRUD()
    return crud.listar()


@router_inscripciones.get(
    "/{id_inscripcion}",
    response_model=InscripcionResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_inscripcion(id_inscripcion: UUID) -> Inscripcion:
    crud = InscripcionCRUD()
    inscripcion = crud.obtener(id_inscripcion)

    if inscripcion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada",
        )

    return inscripcion


@router_inscripciones.post(
    "/",
    response_model=InscripcionResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_inscripcion(datos: InscripcionCreate) -> Inscripcion:
    crud = InscripcionCRUD()

    nueva_inscripcion = Inscripcion(
        estado=datos.estado,
        id_usuario=datos.id_usuario,
        id_curso=datos.id_curso,
    )

    return crud.crear(nueva_inscripcion)


@router_inscripciones.put(
    "/{id_inscripcion}",
    response_model=InscripcionResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_inscripcion(
    id_inscripcion: UUID,
    datos: InscripcionUpdate,
) -> Inscripcion:
    crud = InscripcionCRUD()

    cambios = datos.model_dump(exclude_unset=True)

    inscripcion = crud.actualizar(
        id_inscripcion,
        cambios,
    )

    if inscripcion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada",
        )

    return inscripcion


@router_inscripciones.delete(
    "/{id_inscripcion}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_inscripcion(id_inscripcion: UUID) -> None:
    crud = InscripcionCRUD()

    eliminado = crud.eliminar(id_inscripcion)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada",
        )

    return None

# SCHEMAS DE PROGRESO

class ProgresoCreate(BaseModel):
    porcentaje: float = 0.0
    estado: str = ""
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None
    id_leccion: Optional[UUID] = None


class ProgresoUpdate(BaseModel):
    porcentaje: Optional[float] = None
    estado: Optional[str] = None
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None
    id_leccion: Optional[UUID] = None


class ProgresoResponse(BaseModel):
    id_progreso: UUID
    porcentaje: float
    estado: str
    ultima_actualizacion: datetime
    id_usuario: Optional[UUID] = None
    id_curso: Optional[UUID] = None
    id_leccion: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


# ENDPOINTS DE PROGRESO


@router_progresos.get(
    "/",
    response_model=list[ProgresoResponse],
    status_code=status.HTTP_200_OK,
)
def listar_progresos() -> list[Progreso]:
    crud = ProgresoCRUD()
    return crud.listar()


@router_progresos.get(
    "/{id_progreso}",
    response_model=ProgresoResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_progreso(id_progreso: UUID) -> Progreso:
    crud = ProgresoCRUD()
    progreso = crud.obtener(id_progreso)

    if progreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progreso no encontrado",
        )

    return progreso


@router_progresos.post(
    "/",
    response_model=ProgresoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_progreso(datos: ProgresoCreate) -> Progreso:
    crud = ProgresoCRUD()

    nuevo_progreso = Progreso(
        porcentaje=datos.porcentaje,
        estado=datos.estado,
        id_usuario=datos.id_usuario,
        id_curso=datos.id_curso,
        id_leccion=datos.id_leccion,
    )

    return crud.crear(nuevo_progreso)


@router_progresos.put(
    "/{id_progreso}",
    response_model=ProgresoResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_progreso(
    id_progreso: UUID,
    datos: ProgresoUpdate,
) -> Progreso:
    crud = ProgresoCRUD()

    cambios = datos.model_dump(exclude_unset=True)

    progreso = crud.actualizar(
        id_progreso,
        cambios,
    )

    if progreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progreso no encontrado",
        )

    return progreso


@router_progresos.delete(
    "/{id_progreso}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_progreso(id_progreso: UUID) -> None:
    crud = ProgresoCRUD()

    eliminado = crud.eliminar(id_progreso)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progreso no encontrado",
        )

    return None


# SCHEMAS DE EVALUACIÓN

class EvaluacionCreate(BaseModel):
    nombre: str
    descripcion: str
    calificacion: float = 0.0
    id_leccion: Optional[UUID] = None
    id_usuario: Optional[UUID] = None


class EvaluacionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    calificacion: Optional[float] = None
    id_leccion: Optional[UUID] = None
    id_usuario: Optional[UUID] = None


class EvaluacionResponse(BaseModel):
    id_evaluacion: UUID
    nombre: str
    descripcion: str
    calificacion: float
    id_leccion: Optional[UUID] = None
    id_usuario: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


# ENDPOINTS DE EVALUACIÓN


@router_evaluaciones.get(
    "/",
    response_model=list[EvaluacionResponse],
    status_code=status.HTTP_200_OK,
)
def listar_evaluaciones() -> list[Evaluacion]:
    crud = EvaluacionCRUD()
    return crud.listar()


@router_evaluaciones.get(
    "/{id_evaluacion}",
    response_model=EvaluacionResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_evaluacion(id_evaluacion: UUID) -> Evaluacion:
    crud = EvaluacionCRUD()
    evaluacion = crud.obtener(id_evaluacion)

    if evaluacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada",
        )

    return evaluacion


@router_evaluaciones.post(
    "/",
    response_model=EvaluacionResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_evaluacion(datos: EvaluacionCreate) -> Evaluacion:
    crud = EvaluacionCRUD()

    nueva_evaluacion = Evaluacion(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        calificacion=datos.calificacion,
        id_leccion=datos.id_leccion,
        id_usuario=datos.id_usuario,
    )

    return crud.crear(nueva_evaluacion)


@router_evaluaciones.put(
    "/{id_evaluacion}",
    response_model=EvaluacionResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_evaluacion(
    id_evaluacion: UUID,
    datos: EvaluacionUpdate,
) -> Evaluacion:
    crud = EvaluacionCRUD()

    cambios = datos.model_dump(exclude_unset=True)

    evaluacion = crud.actualizar(
        id_evaluacion,
        cambios,
    )

    if evaluacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada",
        )

    return evaluacion


@router_evaluaciones.delete(
    "/{id_evaluacion}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_evaluacion(id_evaluacion: UUID) -> None:
    crud = EvaluacionCRUD()

    eliminado = crud.eliminar(id_evaluacion)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada",
        )

    return None
