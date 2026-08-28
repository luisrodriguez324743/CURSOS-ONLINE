from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .leccion import Leccion


@dataclass
class Modulo:
    id_modulo: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    orden: int = 0
    id_curso: UUID | None = None

    def pertenece_a(self, id_curso: UUID) -> bool:
        """Indica si este módulo pertenece al curso indicado."""
        return self.id_curso == id_curso

    def agregar_leccion(self, leccion: Leccion) -> None:
        """Asocia una lección a este módulo."""
        leccion.id_modulo = self.id_modulo

    def quitar_leccion(self, leccion: Leccion) -> None:
        """Desasocia una lección si pertenece a este módulo."""
        if leccion.pertenece_a(self.id_modulo):
            leccion.id_modulo = None

    def lecciones_del_modulo(self, lecciones: list[Leccion]) -> list[Leccion]:
        """Obtiene las lecciones asociadas a este módulo."""
        return [leccion for leccion in lecciones if leccion.pertenece_a(self.id_modulo)]

    def contar_lecciones(self, lecciones: list[Leccion]) -> int:
        """Cuenta las lecciones del módulo."""
        return len(self.lecciones_del_modulo(lecciones))

    def calcular_duracion_total(self, lecciones: list[Leccion]) -> int:
        """Calcula la duración total de sus lecciones."""
        return sum(leccion.duracion for leccion in self.lecciones_del_modulo(lecciones))

    def mostrar_modulo(self, lecciones: list[Leccion]) -> None:
        """Muestra el módulo y sus lecciones ordenadas."""
        print(f"- {self.nombre}")
        for leccion in sorted(self.lecciones_del_modulo(lecciones), key=lambda item: item.orden):
            leccion.mostrar_leccion()
