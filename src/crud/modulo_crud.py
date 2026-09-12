from typing import Any
from uuid import UUID

from src.database.connection import get_session
from src.entities.curso import Curso
from src.entities.modulo import Modulo


class ModuloCRUD:
    @staticmethod
    def _leer_opcion(mensaje: str) -> str:
        return input(mensaje).strip()

    def cursos_del_instructor(self, usuario, datos: dict[str, object]) -> list[Curso]:
        return [
            curso
            for curso in datos["cursos"].listar()
            if curso.id_profesor == usuario.id_usuario
        ]

    def crear_curso_instructor(self, usuario, datos: dict[str, object]) -> None:
        try:
            precio = float(self._leer_opcion("Precio del curso: "))
            if precio < 0:
                print("El precio no puede ser negativo.")
                return
        except ValueError:
            print("El precio debe ser un número válido.")
            return

        curso = datos["cursos"].crear_curso(
            nombre=self._leer_opcion("Nombre del curso: "),
            descripcion=self._leer_opcion("Descripción del curso: "),
            precio=precio,
            id_profesor=usuario.id_usuario,
        )
        print(f"Curso creado correctamente: {curso.nombre}")

    def crear_modulo_instructor(self, usuario, datos: dict[str, object]) -> None:
        cursos = self.cursos_del_instructor(usuario, datos)
        if not cursos:
            print("No tienes cursos asignados para crear módulos.")
            return

        print("\nTus cursos:")
        for indice, curso in enumerate(cursos, start=1):
            print(f"{indice}. {curso.nombre}")

        try:
            curso = cursos[int(self._leer_opcion("Selecciona el curso: ")) - 1]
            orden = int(self._leer_opcion("Orden del módulo: "))
        except (ValueError, IndexError):
            print("Selección u orden inválido.")
            return

        modulo = self.crear_para_curso(
            curso,
            self._leer_opcion("Nombre del módulo: "),
            self._leer_opcion("Descripción del módulo: "),
            orden,
        )
        print(f"Módulo creado correctamente: {modulo.nombre}")

    def crear(self, registro: Modulo) -> Modulo:
        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def crear_para_curso(
        self, curso: Curso, nombre: str, descripcion: str = "", orden: int = 0
    ) -> Modulo:
        return self.crear(
            Modulo(
                nombre=nombre,
                descripcion=descripcion,
                orden=orden,
                id_curso=curso.id_curso,
            )
        )

    def listar(self) -> list[Modulo]:
        session = get_session()
        try:
            return session.query(Modulo).all()
        finally:
            session.close()

    def listar_del_curso(self, curso: Curso) -> list[Modulo]:
        session = get_session()
        try:
            return (
                session.query(Modulo)
                .filter_by(id_curso=curso.id_curso)
                .order_by(Modulo.orden)
                .all()
            )
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Modulo | None:
        session = get_session()
        try:
            return session.query(Modulo).filter_by(id_modulo=identificador).first()
        finally:
            session.close()

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Modulo | None:
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(id_modulo=identificador).first()
            if modulo is None:
                return None
            for nombre, valor in cambios.items():
                if nombre == "nombre":
                    modulo.set_nombre(valor)
                elif nombre == "orden":
                    modulo.set_orden(valor)
                elif nombre in {"descripcion", "id_curso"}:
                    setattr(modulo, nombre, valor)
            session.commit()
            session.refresh(modulo)
            return modulo
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(id_modulo=identificador).first()
            if modulo is None:
                return False
            session.delete(modulo)
            session.commit()
            return True
        finally:
            session.close()
