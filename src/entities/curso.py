import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base

if TYPE_CHECKING:
    from .modulo import Modulo
    from .usuario import Usuario


class Curso(Base):
    __tablename__ = "curso"

    id_curso: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    precio: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    id_profesor: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuario.id_usuario"), nullable=True
    )
    profesor: Mapped["Usuario | None"] = relationship(
        "Usuario", foreign_keys=[id_profesor]
    )
    modulos: Mapped[list["Modulo"]] = relationship(
        back_populates="curso", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
        precio: float = 0.0,
        id_profesor: uuid.UUID | None = None,
        id_curso: uuid.UUID | None = None,
    ) -> None:
        self.set_nombre(nombre)
        self.set_descripcion(descripcion)
        self.set_precio(precio)
        self.set_id_profesor(id_profesor)
        if id_curso is not None:
            self.set_id_curso(id_curso)

    def get_id_curso(self) -> uuid.UUID:
        return self.id_curso

    def set_id_curso(self, id_curso: uuid.UUID) -> None:
        self.id_curso = id_curso

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str) -> None:
        if not nombre.strip():
            raise ValueError("El curso debe tener un nombre.")
        self.nombre = nombre

    def get_descripcion(self) -> str:
        return self.descripcion

    def set_descripcion(self, descripcion: str) -> None:
        self.descripcion = descripcion

    def get_precio(self) -> float:
        return self.precio

    def set_precio(self, precio: float) -> None:
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = precio

    def get_id_profesor(self) -> uuid.UUID | None:
        return self.id_profesor

    def set_id_profesor(self, id_profesor: uuid.UUID | None) -> None:
        self.id_profesor = id_profesor

    def agregar_modulo(self, modulo: "Modulo") -> None:
        """Asocia un módulo con este curso."""
        modulo.set_id_curso(self.id_curso)

    def quitar_modulo(self, modulo: "Modulo") -> None:
        """Desasocia un módulo si pertenece a este curso."""
        if modulo.pertenece_a(self.id_curso):
            modulo.set_id_curso(None)

    def modulos_del_curso(self, modulos: list["Modulo"]) -> list["Modulo"]:
        """Obtiene los módulos asociados a este curso."""
        return [modulo for modulo in modulos if modulo.pertenece_a(self.id_curso)]
