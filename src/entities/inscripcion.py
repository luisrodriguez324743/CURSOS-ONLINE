from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Inscripcion:
    id_inscripcion: UUID = field(default_factory=uuid4)
    fecha_inscripcion: datetime = field(default_factory=datetime.now)
    estado: str = ""
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
