from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Usuario:
    id_usuario: UUID = field(default_factory=uuid4)
    nombre: str = ""
    nombre_usuario: str = ""
    correo: str = ""
    password: str = ""
    id_rol: UUID | None = None
    area: str = ""
    activo: bool = True
    fecha_registro: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return (
            f"Usuario({self.nombre_usuario}, {self.correo}, área={self.area}, {estado})"
        )
