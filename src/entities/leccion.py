from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Leccion:
    id_leccion: UUID = field(default_factory=uuid4)
    nombre: str = ""
    contenido: str = ""
    orden: int = 0
    id_modulo: UUID | None = None
    duracion: int = 0

    def pertenece_a(self, id_modulo: UUID) -> bool:
        """Indica si esta lección pertenece al módulo indicado."""
        return self.id_modulo == id_modulo

    def asignar_modulo(self, id_modulo: UUID) -> None:
        """Asocia la lección a un módulo."""
        self.id_modulo = id_modulo

    def quitar_modulo(self) -> None:
        """Desasocia la lección de su módulo."""
        self.id_modulo = None

    def tiene_contenido(self) -> bool:
        """Indica si la lección contiene texto."""
        return bool(self.contenido.strip())

    def mostrar_leccion(self) -> None:
        """Muestra la información básica de la lección."""
        estado = "con contenido" if self.tiene_contenido() else "sin contenido"
        print(f"  · {self.nombre} | {self.duracion} min | {estado}")
