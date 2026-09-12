import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
from src.database.connection import Base, engine
from src.entities.usuario import Usuario
from src.services.app_actions import (
    completar_curso,
    crear_evaluacion_profesor,
    gestionar_resenas,
    iniciar_sesion,
    leer_opcion,
    mostrar_certificados,
    mostrar_historial_pagos,
    nombre_completo,
    procesar_compra_curso,
    registrar_usuario,
)


def inicializar_crud() -> dict[str, object]:
    Base.metadata.create_all(bind=engine)
    roles = RolCRUD()
    rol_estudiante = roles.buscar_por_nombre("Estudiante") or roles.crear(
        "Estudiante", "Usuario que toma cursos"
    )
    rol_profesor = roles.buscar_por_nombre("Profesor") or roles.crear(
        "Profesor", "Usuario que publica cursos"
    )
    return {
        "usuarios": UsuarioCRUD(),
        "roles": roles,
        "resenas": ResenaCRUD(),
        "rol_estudiante": rol_estudiante,
        "rol_profesor": rol_profesor,
        "cursos": CursoCRUD(),
        "inscripciones": InscripcionCRUD(),
        "progresos": ProgresoCRUD(),
        "pagos": PagoCRUD(),
        "modulos": ModuloCRUD(),
        "lecciones": LeccionCRUD(),
        "evaluaciones": EvaluacionCRUD(),
        "facturas": FacturaCRUD(),
        "certificados": CertificadoCRUD(),
    }


def menu_instructor(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print(f"\n--- MENÚ DE INSTRUCTOR ({usuario.nombre_usuario}) ---")
        print("1. Ver mi perfil")
        print("2. Ver cursos")
        print("3. Crear curso")
        print("4. Crear módulo")
        print("5. Crear lección")
        print("6. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            print(f"\nNombre: {nombre_completo(usuario)}")
            print(f"Email: {usuario.correo}")
            print(f"ID Rol: {usuario.id_rol}")
        elif opcion == "2":
            datos["cursos"].mostrar_cursos()
        elif opcion == "3":
            datos["modulos"].crear_curso_instructor(usuario, datos)
        elif opcion == "4":
            datos["modulos"].crear_modulo_instructor(usuario, datos)
        elif opcion == "5":
            datos["lecciones"].crear_leccion_instructor(usuario, datos)
        elif opcion == "6":
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida.")


def menu_profesor(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print(f"\n--- MENÚ DE PROFESOR ({usuario.nombre_usuario}) ---")
        print("1. Ver mi perfil")
        print("2. Crear evaluación")
        print("3. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            print(f"\nNombre: {nombre_completo(usuario)}")
            print(f"Email: {usuario.correo}")
            print(f"ID Rol: {usuario.id_rol}")
        elif opcion == "2":
            crear_evaluacion_profesor(usuario, datos)
        elif opcion == "3":
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida.")


def menu_usuario(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print(f"\n--- MENÚ DE USUARIO ({usuario.nombre_usuario}) ---")
        print("1. Ver mi perfil")
        print("2. Ver cursos")
        print("3. Comprar y acceder a un curso")
        print("4. Ver mis cursos")
        print("5. Ver historial de pagos")
        print("6. Completar curso")
        print("7. Ver certificados")
        print("8. Gestionar mis reseñas")
        print("9. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            print(f"\nNombre: {nombre_completo(usuario)}")
            print(f"Email: {usuario.correo}")
            print(f"ID Rol: {usuario.id_rol}")
        elif opcion == "2":
            datos["cursos"].mostrar_cursos()
        elif opcion == "3":
            procesar_compra_curso(usuario, datos)
        elif opcion == "4":
            datos["cursos"].mostrar_mis_cursos(usuario, datos)
        elif opcion == "5":
            mostrar_historial_pagos(usuario, datos)
        elif opcion == "6":
            completar_curso(usuario, datos)
        elif opcion == "7":
            mostrar_certificados(usuario, datos)
        elif opcion == "8":
            gestionar_resenas(usuario, datos)
        elif opcion == "9":
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
            if usuario is None:
                continue
            rol = datos["roles"].obtener_por_id(usuario.id_rol)
            nombre_rol = rol.nombre_rol.strip().casefold() if rol else ""
            if nombre_rol == "profesor":
                menu_profesor(usuario, datos)
            elif nombre_rol == "instructor":
                menu_instructor(usuario, datos)
            else:
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
