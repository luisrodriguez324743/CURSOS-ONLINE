from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Certificado:
    id_certificado: UUID = field(default_factory=uuid4)
    fecha_emision: datetime = field(default_factory=datetime.now)
    codigo: str = ""
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
