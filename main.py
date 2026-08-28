from src.crud.certificado_crud import CertificadoCRUD
from src.crud.curso_crud import CursoCRUD
from src.crud.evaluacion_crud import EvaluacionCRUD
from src.crud.factura_crud import FacturaCRUD
from src.crud.inscripcion_crud import InscripcionCRUD
from src.crud.leccion_crud import LeccionCRUD
from src.crud.modulo_crud import ModuloCRUD
from src.crud.pago_crud import PagoCRUD
from src.crud.progreso_crud import ProgresoCRUD
from src.entities.inscripcion import Inscripcion
from src.entities.curso import Curso
from src.entities.progreso import Progreso
from src.entities.resena import Resena
from uuid import UUID

# Usuario, Resena, Rol
from src.crud.resena_crud import ResenaCRUD
from src.crud.rol_crud import RolCRUD
from src.crud.usuario_crud import UsuarioCRUD
from src.entities.rol import Rol
from src.entities.usuario import Usuario


# USUARIO, ROL, RESENA
def inicializar_crud() -> dict[str, object]:
    roles = RolCRUD()
    rol_estudiante = roles.crear(
        Rol(nombre="Estudiante", descripcion="Usuario que toma cursos")
    )
    rol_profesor = roles.crear(
        Rol(nombre="Profesor", descripcion="Usuario que publica cursos")
    )

    cursos = CursoCRUD()
    Curso.crear_cursos_iniciales(cursos)

    return {
        # USUARIO; ROL, RESENA
        "usuarios": UsuarioCRUD(),
        "roles": roles,
        "resenas": ResenaCRUD(),
        "rol_estudiante": rol_estudiante,
        "rol_profesor": rol_profesor,
        "cursos": cursos,
        "inscripciones": InscripcionCRUD(),
        "progresos": ProgresoCRUD(),
        "pagos": PagoCRUD(),
        "modulos": ModuloCRUD(),
        "lecciones": LeccionCRUD(),
        "evaluaciones": EvaluacionCRUD(),
        "facturas": FacturaCRUD(),
        "certificados": CertificadoCRUD(),
    }


# USUARIO, ROL, RESENA
def leer_opcion(mensaje: str) -> str:
    return input(mensaje).strip()


def iniciar_sesion(datos: dict[str, object]) -> Usuario | None:
    nombre_usuario = leer_opcion("Nombre de usuario: ")
    password = leer_opcion("Contraseña: ")

    usuario = datos["usuarios"].autenticar(nombre_usuario, password)

    if usuario is None:
        print("Credenciales incorrectas.")
        return None

    # Usamos nombre_usuario o nombre según los atributos de tu entidad Usuario
    print(f"Bienvenido, {usuario.nombre_usuario}.")
    return usuario


def registrar_usuario(datos: dict[str, object]) -> None:
    usuarios: UsuarioCRUD = datos["usuarios"]
    rol_estudiante: Rol = datos["rol_estudiante"]

    nombre_usuario = leer_opcion("Nombre de usuario: ")

    if usuarios.buscar_por_nombre(nombre_usuario) is not None:
        print("Ese nombre de usuario ya existe.")
        return

    usuario = Usuario(
        nombre=leer_opcion("Nombre completo: "),
        nombre_usuario=nombre_usuario,
        correo=leer_opcion("Correo electrónico: "),
        password=leer_opcion("Contraseña: "),
        area=leer_opcion("Área (ej. Sistemas, Educación): "),
        id_rol=rol_estudiante.id_rol,
    )

    usuarios.crear(usuario)
    print(f"Usuario creado correctamente. Tu ID es: {usuario.id_usuario}")


def menu_usuario(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print(f"\n--- MENÚ DE USUARIO ({usuario.nombre_usuario}) ---")
        print("1. Ver mi perfil")
        print("2. Ver cursos")
        print("3. Inscribirme y acceder a un curso")
        print("4. Ver mis cursos")
        print("5. Gestionar mis reseñas")
        print("6. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            print(f"\nNombre: {usuario.nombre}")
            print(f"Email: {usuario.correo}")
            print(f"ID Rol: {usuario.id_rol}")
        elif opcion == "2":
            Curso.mostrar_cursos(datos["cursos"])
        elif opcion == "3":
            Curso.acceder_curso(datos["cursos"], usuario, datos)
        elif opcion == "4":
            Curso.mostrar_mis_cursos(datos["cursos"], usuario, datos)
        elif opcion == "5":
            print("\n[Módulo de Reseñas en construcción]")
        elif opcion == "6":
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida.")


def main() -> None:
    datos = inicializar_crud()
    while True:
        print("\n===== BIENVENIDO =====")
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


def crear_resena_ejemplo(usuario: Usuario, id_curso: UUID, datos: dict) -> None:
    resenas: ResenaCRUD = datos["resenas"]

    calificacion = int(leer_opcion("Calificación (1 a 5): "))
    comentario = leer_opcion("Comentario: ")

    nueva_resena = Resena(
        calificacion=calificacion,
        comentario=comentario,
        id_usuario=usuario.id_usuario,  # Enlazado al usuario con sesión activa
        id_curso=id_curso,
    )

    resenas.crear(nueva_resena)
    print("¡Reseña publicada con éxito!")
