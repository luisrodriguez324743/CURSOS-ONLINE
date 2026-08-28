from src.entities.leccion import Leccion
from src.entities.modulo import Modulo
from .base_crud import CRUD


class LeccionCRUD(CRUD[Leccion]):
    def __init__(self) -> None:
        super().__init__(Leccion)

    def crear(self, registro: Leccion) -> Leccion:
        self.validar(registro)
        return super().crear(registro)

    def validar(self, leccion: Leccion) -> None:
        if not leccion.nombre.strip():
            raise ValueError("La lección debe tener un nombre.")
        if leccion.orden < 0:
            raise ValueError("El orden no puede ser negativo.")
        if leccion.duracion < 0:
            raise ValueError("La duración no puede ser negativa.")

    def crear_para_modulo(
        self,
        modulo: Modulo,
        nombre: str,
        contenido: str = "",
        orden: int = 0,
        duracion: int = 0,
    ) -> Leccion:
        """Construye, valida, registra y asocia una lección."""
        leccion = self.crear(
            Leccion(
                nombre=nombre,
                contenido=contenido,
                orden=orden,
                duracion=duracion,
            )
        )
        modulo.agregar_leccion(leccion)
        return leccion

    def listar_del_modulo(self, modulo: Modulo) -> list[Leccion]:
        """Lista las lecciones pertenecientes al módulo."""
        return modulo.lecciones_del_modulo(self.listar())
