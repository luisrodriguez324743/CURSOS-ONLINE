from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Factura:
    id_factura: UUID = field(default_factory=uuid4)
    numero_factura: str = ""
    fecha_emision: datetime = field(default_factory=datetime.now)
    total: float = 0.0
    id_inscripcion: UUID | None = None
