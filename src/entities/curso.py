from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .modulo import Modulo


@dataclass
class Curso:
    id_curso: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0
    id_profesor: UUID | None = None

    def __post_init__(self) -> None:
        if not self.nombre.strip():
            raise ValueError("El curso debe tener un nombre.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    @classmethod
    def crear_curso(
        cls,
        cursos,
        nombre: str,
        descripcion: str = "",
        precio: float = 0.0,
        id_profesor: UUID | None = None,
    ) -> "Curso":
        return cursos.crear(
            cls(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                id_profesor=id_profesor,
            )
        )

    @classmethod
    def crear_cursos_iniciales(cls, cursos) -> None:
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
            cls.crear_curso(cursos, nombre, descripcion, precio)

    @staticmethod
    def mostrar_cursos(cursos) -> None:
        registros = cursos.listar()
        if not registros:
            print("No hay cursos disponibles.")
            return

        print("\nCursos disponibles:")
        for posicion, curso in enumerate(registros, start=1):
            print(
                f"{posicion}. {curso.nombre} | ${curso.precio:.2f} | {curso.descripcion}"
            )

    @staticmethod
    def acceder_curso(cursos, usuario, datos: dict[str, object]) -> None:
        from src.entities.inscripcion import Inscripcion
        from src.entities.progreso import Progreso

        inscripciones = datos["inscripciones"]
        progresos = datos["progresos"]
        disponibles = cursos.listar()

        if not disponibles:
            print("No hay cursos disponibles.")
            return

        Curso.mostrar_cursos(cursos)
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

    @staticmethod
    def mostrar_mis_cursos(cursos, usuario, datos: dict[str, object]) -> None:
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
            curso = cursos.obtener(inscripcion.id_curso)
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
