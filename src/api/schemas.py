from typing import List, Any, Dict
from uuid import UUID
from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# ESQUEMAS DE USUARIO
# ==========================================

class UsuarioCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    nombre_usuario: str
    correo: EmailStr
    clave: str
    area: str = ""
    id_rol: UUID | None = None


class UsuarioUpdate(BaseModel):
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    nombre_usuario: str | None = None
    correo: EmailStr | None = None
    clave: str | None = None
    area: str | None = None
    activo: bool | None = None
    id_rol: UUID | None = None


class UsuarioRead(BaseModel):
    id_usuario: UUID
    primer_nombre: str
    segundo_nombre: str | None = ""
    primer_apellido: str
    segundo_apellido: str | None = ""
    nombre_usuario: str
    correo: EmailStr
    area: str | None = ""
    activo: bool
    id_rol: UUID | None = None
    fecha_creacion: date
    fecha_edicion: date | None = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    clave: str


class UsuarioList(BaseModel):
    data: List[UsuarioRead]
    status: int
    message: str


class usuarioPost(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class usuarioPut(BaseModel):
    data: UsuarioRead
    status: int
    message: str


# ==========================================
# ESQUEMAS DE ROL
# ==========================================

class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: str | None = None


class RolRead(BaseModel):
    id_rol: UUID
    nombre_rol: str
    descripcion: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RolPost(BaseModel):
    data: RolRead
    status: int
    message: str


class RolList(BaseModel):
    data: List[RolRead]
    status: int
    message: str


# ==========================================
# ESQUEMAS DE RESEÑA
# ==========================================

class ResenaCreate(BaseModel):
    calificacion: int = Field(ge=1, le=5, description="Calificación de 1 a 5")
    id_usuario: UUID
    id_curso: UUID
    comentario: str | None = None


class ResenaUpdate(BaseModel):
    calificacion: int = Field(ge=1, le=5, description="Calificación de 1 a 5")
    comentario: str | None = None


class ResenaRead(BaseModel):
    id_resena: UUID
    calificacion: int
    comentario: str | None = None
    id_usuario: UUID
    id_curso: UUID
    fecha_creacion: date
    fecha_edicion: date | None = None

    model_config = ConfigDict(from_attributes=True)


class ResenaPost(BaseModel):
    data: ResenaRead
    status: int
    message: str


class ResenaPut(BaseModel):
    data: ResenaRead
    status: int
    message: str


class ResenaList(BaseModel):
    data: List[ResenaRead]
    status: int
    message: str


class PromedioResena(BaseModel):
    id_curso: UUID
    promedio: float