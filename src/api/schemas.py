from typing import List
from uuid import UUID
from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr


# ==========================================
# ESQUEMAS DE ENTRADA Y LECTURA
# ==========================================

class UsuarioCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    nombre_usuario: str
    correo: EmailStr  # Valida automáticamente formato de email
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