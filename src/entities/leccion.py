import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base

if TYPE_CHECKING:
    from .modulo import Modulo


class Leccion(Base):
    __tablename__ = "leccion"

    id_leccion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, default="", nullable=False)
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    id_modulo: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("modulo.id_modulo"), nullable=False
    )
    duracion: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    modulo: Mapped["Modulo"] = relationship(back_populates="lecciones")

    def __init__(
        self,
        nombre: str,
        contenido: str = "",
        orden: int = 0,
        id_modulo: uuid.UUID | None = None,
        duracion: int = 0,
        id_leccion: uuid.UUID | None = None,
    ) -> None:
        self.set_nombre(nombre)
        self.set_contenido(contenido)
        self.set_orden(orden)
        self.set_duracion(duracion)
        if id_modulo is not None:
            self.set_id_modulo(id_modulo)
        if id_leccion is not None:
            self.set_id_leccion(id_leccion)

    def get_id_leccion(self) -> uuid.UUID:
        return self.id_leccion

    def set_id_leccion(self, id_leccion: uuid.UUID) -> None:
        self.id_leccion = id_leccion

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str) -> None:
        if not nombre.strip():
            raise ValueError("La lección debe tener un nombre.")
        self.nombre = nombre

    def get_contenido(self) -> str:
        return self.contenido

    def set_contenido(self, contenido: str) -> None:
        self.contenido = contenido

    def get_orden(self) -> int:
        return self.orden

    def set_orden(self, orden: int) -> None:
        if orden < 0:
            raise ValueError("El orden no puede ser negativo.")
        self.orden = orden

    def get_id_modulo(self) -> uuid.UUID | None:
        return self.id_modulo

    def set_id_modulo(self, id_modulo: uuid.UUID | None) -> None:
        self.id_modulo = id_modulo

    def get_duracion(self) -> int:
        return self.duracion

    def set_duracion(self, duracion: int) -> None:
        if duracion < 0:
            raise ValueError("La duración no puede ser negativa.")
        self.duracion = duracion

    def pertenece_a(self, id_modulo: uuid.UUID) -> bool:
        return self.id_modulo == id_modulo

    def asignar_modulo(self, id_modulo: uuid.UUID) -> None:
        self.id_modulo = id_modulo

    def quitar_modulo(self) -> None:
        self.id_modulo = None

    def tiene_contenido(self) -> bool:
        return bool(self.contenido.strip())

    def mostrar_leccion(self) -> None:
        estado = "con contenido" if self.tiene_contenido() else "sin contenido"
        print(f"  · {self.nombre} | {self.duracion} min | {estado}")
