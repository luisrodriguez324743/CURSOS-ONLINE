from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Evaluacion:
    id_evaluacion: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    calificacion: float = 0.0
    id_leccion: UUID | None = None
    id_usuario: UUID | None = None
