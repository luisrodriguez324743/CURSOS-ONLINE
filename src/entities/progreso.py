from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Progreso:
    id_progreso: UUID = field(default_factory=uuid4)
    porcentaje: float = 0.0
    estado: str = ""
    ultima_actualizacion: datetime = field(default_factory=datetime.now)
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
    id_leccion: UUID | None = None
