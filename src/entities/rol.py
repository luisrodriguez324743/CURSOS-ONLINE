from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Usuario:
    id_usuario: UUID = field(default_factory=uuid4)
    nombre: str = ""
    correo: str = ""
    id_rol: UUID = None  # referencia al Rol (FK)
    area: str = ""
    activo: bool = True
    fecha_registro: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"Usuario({self.nombre}, {self.correo}, área={self.area}, {estado})"
