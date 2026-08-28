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
    cursos.crear_cursos_iniciales()

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


def menu_usuario(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print("\n--- MENÚ DE USUARIO ---")
        print("1. Ver cursos")
        print("2. Inscribirme y acceder a un curso")
        print("3. Ver mis cursos")
        print("4. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            datos["cursos"].mostrar_cursos()
        elif opcion == "2":
            datos["cursos"].acceder_curso(usuario, datos)
        elif opcion == "3":
            datos["cursos"].mostrar_mis_cursos(usuario, datos)
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
