from src.entities.modulo import Modulo
from src.entities.curso import Curso
from .base_crud import CRUD


class ModuloCRUD(CRUD[Modulo]):
    def __init__(self) -> None:
        super().__init__(Modulo)

    def crear(self, registro: Modulo) -> Modulo:
        self.validar(registro)
        return super().crear(registro)

    def validar(self, modulo: Modulo) -> None:
        if not modulo.nombre.strip():
            raise ValueError("El módulo debe tener un nombre.")
        if modulo.orden < 0:
            raise ValueError("El orden no puede ser negativo.")

    def crear_para_curso(
        self, curso: Curso, nombre: str, descripcion: str = "", orden: int = 0
    ) -> Modulo:
        """Construye, valida, registra y asocia un módulo."""
        modulo = self.crear(Modulo(nombre=nombre, descripcion=descripcion, orden=orden))
        curso.agregar_modulo(modulo)
        return modulo

    def listar_del_curso(self, curso: Curso) -> list[Modulo]:
        """Lista los módulos pertenecientes al curso."""
        return curso.modulos_del_curso(self.listar())
