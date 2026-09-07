from typing import Any
from uuid import UUID

from src.database.connection import get_session
from src.entities.curso import Curso


class CursoCRUD:

    def crear(self, registro: Curso) -> Curso:
        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def crear_curso(
        self,
        nombre: str,
        descripcion: str = "",
        precio: float = 0.0,
        id_profesor: UUID | None = None,
    ) -> Curso:
        return self.crear(
            Curso(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                id_profesor=id_profesor,
            )
        )

    def crear_cursos_iniciales(self) -> None:
        cursos_iniciales = (
            ("Python desde cero", "Fundamentos del lenguaje Python", 25.0),
            ("Bases de datos", "Modelado y consultas SQL", 30.0),
            (
                "Desarrollo web",
                "Creación de sitios web con HTML, CSS y JavaScript",
                35.0,
            ),
            (
                "Diseño de interfaces",
                "Principios de diseño UX y creación de prototipos",
                28.0,
            ),
        )
        for nombre, descripcion, precio in cursos_iniciales:
            self.crear_curso(nombre, descripcion, precio)

    def mostrar_cursos(self) -> None:
        registros = self.listar()
        if not registros:
            print("No hay cursos disponibles.")
            return

        print("\nCursos disponibles:")
        for posicion, curso in enumerate(registros, start=1):
            print(
                f"{posicion}. {curso.nombre} | ${curso.precio:.2f} | {curso.descripcion}"
            )

    def acceder_curso(self, usuario, datos: dict[str, object]) -> None:
        from src.entities.inscripcion import Inscripcion
        from src.entities.progreso import Progreso

        inscripciones = datos["inscripciones"]
        progresos = datos["progresos"]
        disponibles = self.listar()

        if not disponibles:
            print("No hay cursos disponibles.")
            return

        self.mostrar_cursos()
        try:
            indice = int(input("Selecciona el número del curso: ")) - 1
            curso = disponibles[indice]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        inscrito = next(
            (
                registro
                for registro in inscripciones.listar()
                if registro.id_usuario == usuario.id_usuario
                and registro.id_curso == curso.id_curso
            ),
            None,
        )
        if inscrito is None:
            inscripciones.crear(
                Inscripcion(
                    id_usuario=usuario.id_usuario,
                    id_curso=curso.id_curso,
                    estado="activa",
                )
            )
            progresos.crear(
                Progreso(
                    id_usuario=usuario.id_usuario,
                    id_curso=curso.id_curso,
                    estado="En progreso",
                )
            )
            print(f"Inscripción creada para '{curso.nombre}'.")
        else:
            print(f"Ya estás inscrito en '{curso.nombre}'.")

        print(f"Accediendo al curso: {curso.nombre}")
        print(f"Descripción: {curso.descripcion}")
        print("Tu progreso está disponible en la opción 'Mis cursos'.")

    def mostrar_mis_cursos(self, usuario, datos: dict[str, object]) -> None:
        inscripciones = [
            registro
            for registro in datos["inscripciones"].listar()
            if registro.id_usuario == usuario.id_usuario
        ]
        if not inscripciones:
            print("Todavía no tienes cursos inscritos.")
            return

        print("\nMis cursos:")
        for inscripcion in inscripciones:
            curso = self.obtener(inscripcion.id_curso)
            progreso = next(
                (
                    registro
                    for registro in datos["progresos"].listar()
                    if registro.id_usuario == usuario.id_usuario
                    and registro.id_curso == inscripcion.id_curso
                ),
                None,
            )
            porcentaje = progreso.porcentaje if progreso else 0.0
            print(f"- {curso.nombre} | {porcentaje:.0f}% | {inscripcion.estado}")

    def listar(self) -> list[Curso]:
        session = get_session()
        try:
            return session.query(Curso).all()
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Curso | None:
        session = get_session()
        try:
            return session.query(Curso).filter_by(id_curso=identificador).first()
        finally:
            session.close()

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Curso | None:
        session = get_session()
        try:
            curso = session.query(Curso).filter_by(id_curso=identificador).first()
            if curso is None:
                return None

            for nombre, valor in cambios.items():
                if nombre == "nombre":
                    curso.set_nombre(valor)
                elif nombre == "precio":
                    curso.set_precio(valor)
                elif nombre in {"descripcion", "id_profesor"}:
                    setattr(curso, nombre, valor)
            session.commit()
            session.refresh(curso)
            return curso
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            curso = session.query(Curso).filter_by(id_curso=identificador).first()
            if curso is None:
                return False
            session.delete(curso)
            session.commit()
            return True
        finally:
            session.close()
