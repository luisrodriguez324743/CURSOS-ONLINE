from typing import Any
from uuid import UUID

from src.database.connection import get_session
from src.entities.leccion import Leccion
from src.entities.modulo import Modulo


class LeccionCRUD:
    @staticmethod
    def _leer_opcion(mensaje: str) -> str:
        return input(mensaje).strip()

    def crear_leccion_instructor(self, usuario, datos: dict[str, object]) -> None:
        cursos = datos["modulos"].cursos_del_instructor(usuario, datos)
        modulos = [
            modulo
            for modulo in datos["modulos"].listar()
            if any(curso.id_curso == modulo.id_curso for curso in cursos)
        ]
        if not modulos:
            print("No tienes módulos para crear lecciones.")
            return

        print("\nTus módulos:")
        for indice, modulo in enumerate(modulos, start=1):
            print(f"{indice}. {modulo.nombre}")

        try:
            modulo = modulos[int(self._leer_opcion("Selecciona el módulo: ")) - 1]
            orden = int(self._leer_opcion("Orden de la lección: "))
            duracion = int(self._leer_opcion("Duración en minutos: "))
        except (ValueError, IndexError):
            print("Selección, orden o duración inválidos.")
            return

        leccion = self.crear_para_modulo(
            modulo,
            self._leer_opcion("Nombre de la lección: "),
            self._leer_opcion("Contenido de la lección: "),
            orden,
            duracion,
        )
        print(f"Lección creada correctamente: {leccion.nombre}")

    def crear(self, registro: Leccion) -> Leccion:
        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def crear_para_modulo(
        self,
        modulo: Modulo,
        nombre: str,
        contenido: str = "",
        orden: int = 0,
        duracion: int = 0,
    ) -> Leccion:
        return self.crear(
            Leccion(
                nombre=nombre,
                contenido=contenido,
                orden=orden,
                id_modulo=modulo.id_modulo,
                duracion=duracion,
            )
        )

    def listar(self) -> list[Leccion]:
        session = get_session()
        try:
            return session.query(Leccion).all()
        finally:
            session.close()

    def listar_del_modulo(self, modulo: Modulo) -> list[Leccion]:
        session = get_session()
        try:
            return (
                session.query(Leccion)
                .filter_by(id_modulo=modulo.id_modulo)
                .order_by(Leccion.orden)
                .all()
            )
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Leccion | None:
        session = get_session()
        try:
            return session.query(Leccion).filter_by(id_leccion=identificador).first()
        finally:
            session.close()

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Leccion | None:
        session = get_session()
        try:
            leccion = session.query(Leccion).filter_by(id_leccion=identificador).first()
            if leccion is None:
                return None
            for nombre, valor in cambios.items():
                if nombre == "nombre":
                    leccion.set_nombre(valor)
                elif nombre == "orden":
                    leccion.set_orden(valor)
                elif nombre == "duracion":
                    leccion.set_duracion(valor)
                elif nombre in {"contenido", "id_modulo"}:
                    setattr(leccion, nombre, valor)
            session.commit()
            session.refresh(leccion)
            return leccion
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            leccion = session.query(Leccion).filter_by(id_leccion=identificador).first()
            if leccion is None:
                return False
            session.delete(leccion)
            session.commit()
            return True
        finally:
            session.close()
