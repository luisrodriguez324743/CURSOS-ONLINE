from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Modulo:
    id_modulo: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    orden: int = 0
    id_curso: UUID | None = None
