from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Pago:
    id_pago: UUID = field(default_factory=uuid4)
    monto: float = 0.0
    fecha_pago: datetime = field(default_factory=datetime.now)
    metodo_pago: str = ""
    estado: str = ""
    id_usuario: UUID | None = None
