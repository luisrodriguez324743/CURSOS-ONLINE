from src.crud.certificado_crud import CertificadoCRUD
from src.crud.curso_crud import CursoCRUD
from src.crud.evaluacion_crud import EvaluacionCRUD
from src.crud.factura_crud import FacturaCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud.leccion_crud import LeccionCRUD
from src.crud.modulo_crud import ModuloCRUD
from src.crud.pago_crud import PagoCRUD
from src.crud.progreso_crud import ProgresoCRUD
from src.crud.resena_crud import ResenaCRUD
from src.crud.rol_crud import RolCRUD
from src.crud.usuario_crud import UsuarioCRUD
from src.entities.curso import Curso
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso
from src.entities.rol import Rol
from src.entities.usuario import Usuario


def inicializar_crud() -> dict[str, object]:
    roles = RolCRUD()
    rol_estudiante = roles.crear(
        Rol(nombre="Estudiante", descripcion="Usuario que toma cursos")
    )
    rol_profesor = roles.crear(
        Rol(nombre="Profesor", descripcion="Usuario que publica cursos")
    )

    cursos = CursoCRUD()
    cursos.crear(
        Curso(
            nombre="Python desde cero",
            descripcion="Fundamentos del lenguaje Python",
            precio=25.0,
            id_profesor=None,
        )
    )
    cursos.crear(
        Curso(
            nombre="Bases de datos",
            descripcion="Modelado y consultas SQL",
            precio=30.0,
            id_profesor=None,
        )
    )

    return {
        "usuarios": UsuarioCRUD(),
        "roles": roles,
        "cursos": cursos,
        "inscripciones": InscripcionCRUD(),
        "progresos": ProgresoCRUD(),
        "pagos": PagoCRUD(),
        "modulos": ModuloCRUD(),
        "lecciones": LeccionCRUD(),
        "evaluaciones": EvaluacionCRUD(),
        "facturas": FacturaCRUD(),
        "resenas": ResenaCRUD(),
        "certificados": CertificadoCRUD(),
        "rol_estudiante": rol_estudiante,
        "rol_profesor": rol_profesor,
    }


def leer_opcion(mensaje: str) -> str:
    return input(mensaje).strip()


def mostrar_cursos(cursos: CursoCRUD) -> None:
    disponibles = cursos.listar()
    if not disponibles:
        print("No hay cursos disponibles.")
        return

    print("\nCursos disponibles:")
    for posicion, curso in enumerate(disponibles, start=1):
        print(f"{posicion}. {curso.nombre} | ${curso.precio:.2f} | {curso.descripcion}")


def registrar_usuario(datos: dict[str, object]) -> None:
    usuarios = datos["usuarios"]
    rol_estudiante = datos["rol_estudiante"]
    nombre_usuario = leer_opcion("Nombre de usuario: ")

    if usuarios.buscar_por_nombre(nombre_usuario) is not None:
        print("Ese nombre de usuario ya existe.")
        return

    usuario = Usuario(
        primer_nombre=leer_opcion("Primer nombre: "),
        segundo_nombre=leer_opcion("Segundo nombre (opcional): "),
        primer_apellido=leer_opcion("Primer apellido: "),
        segundo_apellido=leer_opcion("Segundo apellido (opcional): "),
        nombre_usuario=nombre_usuario,
        password=leer_opcion("Contraseña: "),
        id_rol=rol_estudiante.id_rol,
    )
    usuarios.crear(usuario)
    print(f"Usuario creado correctamente. Tu ID es {usuario.id_usuario}")


def iniciar_sesion(datos: dict[str, object]) -> Usuario | None:
    nombre_usuario = leer_opcion("Nombre de usuario: ")
    password = leer_opcion("Contraseña: ")
    usuario = datos["usuarios"].autenticar(nombre_usuario, password)
    if usuario is None:
        print("Credenciales incorrectas.")
        return None
    print(f"Bienvenido, {usuario.primer_nombre}.")
    return usuario


def acceder_curso(usuario: Usuario, datos: dict[str, object]) -> None:
    cursos = datos["cursos"]
    inscripciones = datos["inscripciones"]
    progresos = datos["progresos"]
    disponibles = cursos.listar()
    mostrar_cursos(cursos)
    if not disponibles:
        return

    try:
        indice = int(leer_opcion("Selecciona el número del curso: ")) - 1
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
        inscripcion = inscripciones.crear(
            Inscripcion(
                id_usuario=usuario.id_usuario, id_curso=curso.id_curso, estado="activa"
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


def mostrar_mis_cursos(usuario: Usuario, datos: dict[str, object]) -> None:
    cursos = datos["cursos"]
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


def menu_usuario(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print("\n--- MENÚ DE USUARIO ---")
        print("1. Ver cursos")
        print("2. Inscribirme y acceder a un curso")
        print("3. Ver mis cursos")
        print("4. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            mostrar_cursos(datos["cursos"])
        elif opcion == "2":
            acceder_curso(usuario, datos)
        elif opcion == "3":
            mostrar_mis_cursos(usuario, datos)
        elif opcion == "4":
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida.")


def main() -> None:
    datos = inicializar_crud()
    while True:
        print("\n===== CURSOS ONLINE =====")
        print("1. Iniciar sesión")
        print("2. Crear usuario")
        print("3. Salir")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            usuario = iniciar_sesion(datos)
            if usuario is not None:
                menu_usuario(usuario, datos)
        elif opcion == "2":
            registrar_usuario(datos)
        elif opcion == "3":
            print("Hasta pronto.")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
