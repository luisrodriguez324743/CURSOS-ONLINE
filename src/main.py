import sys
from pathlib import Path
from uuid import UUID

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
from src.entities.certificado import Certificado
from src.entities.curso import Curso
from src.entities.factura import Factura
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago
from src.entities.progreso import Progreso
from src.entities.resena import Resena
from src.entities.rol import Rol
from src.entities.usuario import Usuario


# USUARIO, ROL, RESENA
def inicializar_crud() -> dict[str, object]:
    roles = RolCRUD()
    rol_estudiante = roles.buscar_por_nombre("Estudiante") or roles.crear(
        "Estudiante", "Usuario que toma cursos"
    )
    rol_profesor = roles.buscar_por_nombre("Profesor") or roles.crear(
        "Profesor", "Usuario que publica cursos"
    )

    cursos = CursoCRUD()
    cursos.crear_cursos_iniciales()

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


def nombre_completo(usuario: Usuario) -> str:
    nombres = " ".join(
        parte for parte in (usuario.primer_nombre, usuario.segundo_nombre) if parte
    )
    apellidos = " ".join(
        parte for parte in (usuario.primer_apellido, usuario.segundo_apellido) if parte
    )
    return f"{nombres} {apellidos}".strip()


def iniciar_sesion(datos: dict[str, object]) -> Usuario | None:
    roles: RolCRUD = datos["roles"]
    roles_disponibles = sorted(roles.listar(), key=lambda rol: rol.nombre_rol.lower())

    if not roles_disponibles:
        print("No hay roles disponibles para iniciar sesión.")
        return None

    print("\nRoles disponibles:")
    for indice, rol in enumerate(roles_disponibles, start=1):
        print(f"{indice}. {rol.nombre_rol}")

    try:
        indice_rol = int(leer_opcion("Selecciona tu rol: ")) - 1
        rol_seleccionado = roles_disponibles[indice_rol]
    except (ValueError, IndexError):
        print("Selección de rol inválida.")
        return None

    nombre_usuario = leer_opcion("Nombre de usuario: ")
    password = leer_opcion("Contraseña: ")

    usuario = datos["usuarios"].autenticar(nombre_usuario, password)

    if usuario is None or usuario.id_rol != rol_seleccionado.id_rol:
        print("Credenciales incorrectas.")
        return None

    print(f"Bienvenido, {usuario.nombre_usuario}. Rol: {rol_seleccionado.nombre_rol}")
    return usuario


def registrar_usuario(datos: dict[str, object]) -> None:
    usuarios: UsuarioCRUD = datos["usuarios"]
    roles: RolCRUD = datos["roles"]
    nombres_roles = ("Instructor", "Administrador", "Estudiante", "Profesor")
    roles_por_nombre = {rol.nombre_rol.casefold(): rol for rol in roles.listar()}
    roles_disponibles = [
        roles_por_nombre[nombre.casefold()]
        for nombre in nombres_roles
        if nombre.casefold() in roles_por_nombre
    ]

    if not roles_disponibles:
        print("No hay roles disponibles para registrar el usuario.")
        return

    print("\nSelecciona el rol del usuario:")
    for indice, rol in enumerate(roles_disponibles, start=1):
        print(f"{indice}. {rol.nombre_rol}")

    try:
        rol_seleccionado = roles_disponibles[int(leer_opcion("Rol: ")) - 1]
    except (ValueError, IndexError):
        print("Selección de rol inválida.")
        return

    nombre_usuario = leer_opcion("Nombre de usuario: ")

    if usuarios.buscar_por_nombre(nombre_usuario) is not None:
        print("Ese nombre de usuario ya existe.")
        return

    usuario = usuarios.crear(
        primer_nombre=leer_opcion("Primer nombre: "),
        primer_apellido=leer_opcion("Primer apellido: "),
        nombre_usuario=nombre_usuario,
        correo=leer_opcion("Correo electrónico: "),
        clave=leer_opcion("Contraseña: "),
        id_rol=rol_seleccionado.id_rol,
    )

    if usuario is None:
        print("No se pudo crear el usuario: el nombre o correo ya existe.")
        return
    print(f"Usuario creado correctamente. Tu ID es: {usuario.id_usuario}")


def procesar_compra_curso(usuario: Usuario, datos: dict[str, object]) -> None:
    cursos = datos["cursos"]
    pagos = datos["pagos"]
    facturas = datos["facturas"]
    inscripciones = datos["inscripciones"]
    progresos = datos["progresos"]

    cursos.mostrar_cursos()
    disponibles = cursos.listar()
    if not disponibles:
        return

    try:
        indice = int(leer_opcion("Selecciona el número del curso a comprar: ")) - 1
        curso = disponibles[indice]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    ya_inscrito = next(
        (
            registro
            for registro in inscripciones.listar()
            if registro.id_usuario == usuario.id_usuario
            and registro.id_curso == curso.id_curso
        ),
        None,
    )
    if ya_inscrito is not None:
        print(f"Ya adquiriste '{curso.nombre}' anteriormente.")
        return

    print(f"\nCurso: {curso.nombre}")
    print(f"Precio: ${curso.precio:.2f}")
    metodo = leer_opcion("Método de pago (tarjeta/transferencia/efectivo): ").lower()
    if not metodo:
        metodo = "efectivo"

    referencia = None
    if metodo == "tarjeta":
        referencia = leer_opcion("Número de tarjeta (13 a 19 dígitos): ")
        ok, mensaje = Pago.validar_pago(metodo, referencia)
        if not ok:
            print(mensaje)
            return
    else:
        ok, mensaje = Pago.validar_pago(metodo)
        if not ok:
            print(mensaje)
            return
        print(mensaje)

    pago = pagos.crear(
        Pago.crear_pago(
            monto=curso.precio,
            metodo_pago=metodo,
            id_usuario=usuario.id_usuario,
            id_curso=curso.id_curso,
        )
    )
    factura = facturas.crear(
        Factura.crear_factura(
            total=curso.precio,
            id_usuario=usuario.id_usuario,
            id_curso=curso.id_curso,
            metodo_pago=metodo,
        )
    )
    pago.id_factura = factura.id_factura
    factura.estado = "pagada"

    inscripcion = inscripciones.crear(
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
            porcentaje=0.0,
            estado="En progreso",
        )
    )

    print(factura.generar_comprobante(curso.nombre, nombre_completo(usuario)))
    print(f"ID de inscripción: {inscripcion.id_inscripcion}")
    print(f"Estado del pago: {pago.estado}")
    print("Compra realizada con éxito.")


def mostrar_historial_pagos(usuario: Usuario, datos: dict[str, object]) -> None:
    pagos = [
        registro
        for registro in datos["pagos"].listar()
        if registro.id_usuario == usuario.id_usuario
    ]

    if not pagos:
        print("Todavía no tienes pagos registrados.")
        return

    print("\nHistorial de pagos:")
    for pago in pagos:
        print(f"- {pago.resumen()}")


def emitir_certificado_curso(
    usuario: Usuario, datos: dict[str, object], id_curso: UUID | None = None
) -> None:
    cursos = datos["cursos"].listar()
    if not cursos:
        print("No hay cursos para evaluar.")
        return

    inscripciones = [
        registro
        for registro in datos["inscripciones"].listar()
        if registro.id_usuario == usuario.id_usuario
    ]
    if not inscripciones:
        print("Primero debes inscribirte en un curso.")
        return

    if id_curso is None:
        print("\nCursos inscritos:")
        for idx, inscripcion in enumerate(inscripciones, start=1):
            curso = datos["cursos"].obtener(inscripcion.id_curso)
            print(f"{idx}. {curso.nombre}")

        try:
            opcion = (
                int(leer_opcion("Selecciona el curso para comprobar certificado: ")) - 1
            )
            inscripcion = inscripciones[opcion]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return
        id_curso = inscripcion.id_curso

    curso = datos["cursos"].obtener(id_curso)
    if curso is None:
        print("El curso seleccionado no existe.")
        return

    certificado = Certificado.emitir_si_aplica(
        pagos=list(datos["pagos"].listar()),
        facturas=list(datos["facturas"].listar()),
        progresos=list(datos["progresos"].listar()),
        id_usuario=usuario.id_usuario,
        id_curso=curso.id_curso,
    )
    if certificado is None:
        return

    certs = datos["certificados"]
    certs.crear(certificado)
    print("\n============================")
    print("CERTIFICADO EMITIDO")
    print("============================")
    print(f"Curso: {curso.nombre}")
    print(f"Estudiante: {nombre_completo(usuario)}")
    print(f"Código: {certificado.codigo}")
    print(f"Fecha: {certificado.fecha_emision.strftime('%d/%m/%Y')}")
    print("Se declara que el curso fue culminado satisfactoriamente.")
    print("============================")


def mostrar_certificados(usuario: Usuario, datos: dict[str, object]) -> None:
    certificados = [
        cert
        for cert in datos["certificados"].listar()
        if cert.id_usuario == usuario.id_usuario
    ]

    if not certificados:
        print("Todavía no tienes certificados emitidos.")
        return

    print("\nCertificados emitidos:")
    for cert in certificados:
        curso = datos["cursos"].obtener(cert.id_curso)
        nombre_curso = curso.nombre if curso else "Curso desconocido"
        print(
            f"- {nombre_curso} | {cert.codigo} | {cert.fecha_emision.strftime('%d/%m/%Y')}"
        )


def completar_curso(usuario: Usuario, datos: dict[str, object]) -> None:
    inscripciones = [
        registro
        for registro in datos["inscripciones"].listar()
        if registro.id_usuario == usuario.id_usuario
    ]
    if not inscripciones:
        print("No tienes cursos inscritos.")
        return

    print("\nCursos inscritos:")
    for idx, inscripcion in enumerate(inscripciones, start=1):
        curso = datos["cursos"].obtener(inscripcion.id_curso)
        print(f"{idx}. {curso.nombre}")

    try:
        opcion = int(leer_opcion("Selecciona el curso que deseas culminar: ")) - 1
        inscripcion = inscripciones[opcion]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    progreso = next(
        (
            registro
            for registro in datos["progresos"].listar()
            if registro.id_usuario == usuario.id_usuario
            and registro.id_curso == inscripcion.id_curso
        ),
        None,
    )
    if progreso is None:
        print("No existe progreso para este curso.")
        return

    progreso.porcentaje = 100.0
    progreso.estado = "Completado"
    print(
        f"Curso marcado como completado: {datos['cursos'].obtener(inscripcion.id_curso).nombre}"
    )
    certificado = Certificado.emitir_si_aplica(
        pagos=list(datos["pagos"].listar()),
        facturas=list(datos["facturas"].listar()),
        progresos=list(datos["progresos"].listar()),
        id_usuario=usuario.id_usuario,
        id_curso=inscripcion.id_curso,
    )
    if certificado is not None:
        datos["certificados"].crear(certificado)
        print("\n¿Deseas ver el certificado ahora? (s/n)")
        respuesta = leer_opcion("Respuesta: ").lower()
        if respuesta == "s":
            print("\n============================")
            print("CERTIFICADO EMITIDO")
            print("============================")
            print(f"Curso: {datos['cursos'].obtener(inscripcion.id_curso).nombre}")
            print(f"Estudiante: {nombre_completo(usuario)}")
            print(f"Código: {certificado.codigo}")
            print(f"Fecha: {certificado.fecha_emision.strftime('%d/%m/%Y')}")
            print("Se declara que el curso fue culminado satisfactoriamente.")
            print("============================")
        else:
            print("Puedes revisarlo después desde la opción 'Ver certificados'.")


def menu_instructor(usuario: Usuario, datos: dict[str, object]) -> None:
    while True:
        print(f"\n--- MENÚ DE INSTRUCTOR ({usuario.nombre_usuario}) ---")
        print("1. Ver mi perfil")
        print("2. Crear curso")
        print("3. Crear módulo")
        print("4. Crear lección")
        print("5. Cerrar sesión")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            print(f"\nNombre: {nombre_completo(usuario)}")
            print(f"Email: {usuario.correo}")
            print(f"ID Rol: {usuario.id_rol}")
        elif opcion == "2":
            datos["modulos"].crear_curso_instructor(usuario, datos)
        elif opcion == "3":
            datos["modulos"].crear_modulo_instructor(usuario, datos)
        elif opcion == "4":
            datos["lecciones"].crear_leccion_instructor(usuario, datos)
        elif opcion == "5":
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
            print("\n[Módulo de Reseñas en construcción]")
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
            if usuario is not None:
                rol = datos["roles"].obtener_por_id(usuario.id_rol)
                if rol is not None and rol.nombre_rol.casefold() == "instructor":
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
