from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Rol:
    id_rol: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""

    def __str__(self) -> str:
        return f"Rol({self.nombre})"
