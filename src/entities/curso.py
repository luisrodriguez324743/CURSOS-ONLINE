from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Curso:
    id_curso: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0
    id_profesor: UUID | None = None
