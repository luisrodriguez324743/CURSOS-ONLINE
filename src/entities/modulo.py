import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base

if TYPE_CHECKING:
    from .leccion import Leccion


class Modulo(Base):
    __tablename__ = "modulo"

    id_modulo: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    id_curso: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("curso.id_curso"), nullable=False
    )

    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
        orden: int = 0,
        id_curso: uuid.UUID | None = None,
        id_modulo: uuid.UUID | None = None,
    ) -> None:
        self.set_nombre(nombre)
        self.set_descripcion(descripcion)
        self.set_orden(orden)
        if id_curso is not None:
            self.set_id_curso(id_curso)
        if id_modulo is not None:
            self.set_id_modulo(id_modulo)

    def get_id_modulo(self) -> uuid.UUID:
        return self.id_modulo

    def set_id_modulo(self, id_modulo: uuid.UUID) -> None:
        self.id_modulo = id_modulo

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str) -> None:
        if not nombre.strip():
            raise ValueError("El módulo debe tener un nombre.")
        self.nombre = nombre

    def get_descripcion(self) -> str:
        return self.descripcion

    def set_descripcion(self, descripcion: str) -> None:
        self.descripcion = descripcion

    def get_orden(self) -> int:
        return self.orden

    def set_orden(self, orden: int) -> None:
        if orden < 0:
            raise ValueError("El orden no puede ser negativo.")
        self.orden = orden

    def get_id_curso(self) -> uuid.UUID | None:
        return self.id_curso

    def set_id_curso(self, id_curso: uuid.UUID | None) -> None:
        self.id_curso = id_curso

    def pertenece_a(self, id_curso: uuid.UUID) -> bool:
        return self.id_curso == id_curso

    def agregar_leccion(self, leccion: "Leccion") -> None:
        leccion.set_id_modulo(self.id_modulo)

    def quitar_leccion(self, leccion: "Leccion") -> None:
        if leccion.pertenece_a(self.id_modulo):
            leccion.set_id_modulo(None)

    def lecciones_del_modulo(self, lecciones: list["Leccion"]) -> list["Leccion"]:
        return [leccion for leccion in lecciones if leccion.pertenece_a(self.id_modulo)]

    def contar_lecciones(self, lecciones: list["Leccion"]) -> int:
        return len(self.lecciones_del_modulo(lecciones))

    def calcular_duracion_total(self, lecciones: list["Leccion"]) -> int:
        return sum(leccion.duracion for leccion in self.lecciones_del_modulo(lecciones))

    def mostrar_modulo(self, lecciones: list["Leccion"]) -> None:
        print(f"- {self.nombre}")
        for leccion in sorted(
            self.lecciones_del_modulo(lecciones), key=lambda item: item.orden
        ):
            leccion.mostrar_leccion()
