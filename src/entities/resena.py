from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Resena:
    id_resena: UUID = field(default_factory=uuid4)
    calificacion: int = 5
    comentario: str = ""
    fecha: datetime = field(default_factory=datetime.now)
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
