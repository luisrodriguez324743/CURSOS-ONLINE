from src.entities.curso import Curso
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso
from src.entities.usuario import Usuario
from .base_crud import CRUD


class CursoCRUD(CRUD[Curso]):
    def __init__(self) -> None:
        super().__init__(Curso)

    def crear(self, registro: Curso) -> Curso:
        self.validar(registro)
        return super().crear(registro)

    def validar(self, curso: Curso) -> None:
        if not curso.nombre.strip():
            raise ValueError("El curso debe tener un nombre.")
        if curso.precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    def crear_curso(
        self, nombre: str, descripcion: str = "", precio: float = 0.0, id_profesor=None
    ) -> Curso:
        """Construye, valida y registra un curso."""
        return self.crear(
            Curso(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                id_profesor=id_profesor,
            )
        )

    def crear_cursos_iniciales(self) -> None:
        """Crea los cursos disponibles al iniciar la aplicación."""
        cursos_iniciales = (
            (
                "Python desde cero",
                "Fundamentos del lenguaje Python",
                25.0,
            ),
            (
                "Bases de datos",
                "Modelado y consultas SQL",
                30.0,
            ),
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

    def disponibles(self) -> list[Curso]:
        """Lista los cursos publicados y válidos."""
        return [curso for curso in self.listar() if curso.esta_disponible()]

    def obtener_disponible(self, indice: int) -> Curso | None:
        """Obtiene un curso disponible por índice."""
        disponibles = self.disponibles()
        return disponibles[indice] if 0 <= indice < len(disponibles) else None

    def mostrar_cursos(self) -> None:
        """Muestra todos los cursos registrados."""
        cursos = self.listar()
        if not cursos:
            print("No hay cursos disponibles.")
            return

        print("\nCursos disponibles:")
        for posicion, curso in enumerate(cursos, start=1):
            print(
                f"{posicion}. {curso.nombre} | ${curso.precio:.2f} | "
                f"{curso.descripcion}"
            )

    def acceder_curso(self, usuario: Usuario, datos: dict[str, object]) -> None:
        """Muestra cursos, registra la inscripción y crea el progreso inicial."""
        inscripciones = datos["inscripciones"]
        progresos = datos["progresos"]
        disponibles = self.listar()

        if not disponibles:
            print("No hay cursos disponibles.")
            return

        print("\nCursos disponibles:")
        for posicion, curso in enumerate(disponibles, start=1):
            print(
                f"{posicion}. {curso.nombre} | ${curso.precio:.2f} | {curso.descripcion}"
            )

        try:
            indice = int(input("Selecciona el número del curso: ")) - 1
            curso = disponibles[indice]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        inscripcion = next(
            (
                registro
                for registro in inscripciones.listar()
                if registro.id_usuario == usuario.id_usuario
                and registro.id_curso == curso.id_curso
            ),
            None,
        )
        if inscripcion is None:
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

    def mostrar_mis_cursos(self, usuario: Usuario, datos: dict[str, object]) -> None:
        """Muestra los cursos inscritos por el usuario y su progreso."""
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
