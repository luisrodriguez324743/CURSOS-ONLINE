from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Leccion:
    id_leccion: UUID = field(default_factory=uuid4)
    nombre: str = ""
    contenido: str = ""
    orden: int = 0
    id_modulo: UUID | None = None
