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
        roles_profesor = {
            rol.id_rol
            for rol in datos["roles"].listar()
            if rol.nombre_rol.strip().casefold() == "profesor"
        }
        profesores = [
            profesor
            for profesor in datos["usuarios"].listar()
            if profesor.id_rol in roles_profesor
        ]
        profesores.sort(key=lambda profesor: profesor.nombre_usuario.casefold())

        if not profesores:
            print("No hay profesores disponibles para asociar el curso.")
            return

        print("\nSelecciona el profesor del curso:")
        for indice, profesor in enumerate(profesores, start=1):
            print(
                f"{indice}. {profesor.nombre_usuario} - "
                f"{profesor.primer_nombre} {profesor.primer_apellido}"
            )
        try:
            profesor = profesores[int(self._leer_opcion("Profesor: ")) - 1]
        except (ValueError, IndexError):
            print("Selección de profesor inválida.")
            return

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
            id_profesor=profesor.id_usuario,
        )
        print(
            f"Curso creado correctamente: {curso.nombre}. "
            f"Profesor asignado: {profesor.nombre_usuario}"
        )

    def crear_modulo_instructor(self, usuario, datos: dict[str, object]) -> None:
        cursos = datos["cursos"].listar()
        if not cursos:
            print("No hay cursos disponibles para crear módulos.")
            return

        print("\nCursos disponibles:")
        for indice, curso in enumerate(cursos, start=1):
            profesor = (
                datos["usuarios"].obtener_por_id(curso.id_profesor)
                if curso.id_profesor
                else None
            )
            nombre_profesor = profesor.nombre_usuario if profesor else "Sin profesor"
            print(f"{indice}. {curso.nombre} | Profesor: {nombre_profesor}")

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
        print(
            f"Módulo creado correctamente: {modulo.nombre} "
            f"en el curso '{curso.nombre}'."
        )

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
