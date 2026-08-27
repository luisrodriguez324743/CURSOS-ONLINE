from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Usuario:
    id_usuario: UUID = field(default_factory=uuid4)
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    nombre_usuario: str = ""
    password: str = ""
    id_rol: UUID | None = None
