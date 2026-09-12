from uuid import UUID

from src.crud.certificado_crud import CertificadoCRUD
from src.crud.factura_crud import FacturaCRUD
from src.crud.pago_crud import PagoCRUD
from src.crud.rol_crud import RolCRUD
from src.crud.usuario_crud import UsuarioCRUD
from src.entities.evaluacion import Evaluacion
from src.entities.factura import Factura
from src.entities.inscripcion import Inscripcion
from src.entities.progreso import Progreso
from src.entities.resena import Resena
from src.entities.usuario import Usuario


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
        rol = roles_disponibles[int(leer_opcion("Selecciona tu rol: ")) - 1]
    except (ValueError, IndexError):
        print("Selección de rol inválida.")
        return None

    usuario = datos["usuarios"].autenticar(
        leer_opcion("Nombre de usuario: "), leer_opcion("Contraseña: ")
    )
    if usuario is None or usuario.id_rol != rol.id_rol:
        print("Credenciales incorrectas.")
        return None
    print(f"Bienvenido, {usuario.nombre_usuario}. Rol: {rol.nombre_rol}")
    return usuario


def registrar_usuario(datos: dict[str, object]) -> None:
    usuarios: UsuarioCRUD = datos["usuarios"]
    roles: RolCRUD = datos["roles"]
    nombres_roles = ("Instructor", "Administrador", "Estudiante", "Profesor")
    roles_por_nombre = {
        rol.nombre_rol.strip().casefold(): rol for rol in roles.listar()
    }
    disponibles = [
        roles_por_nombre[nombre.casefold()]
        for nombre in nombres_roles
        if nombre.casefold() in roles_por_nombre
    ]
    if not disponibles:
        print("No hay roles disponibles para registrar el usuario.")
        return

    print("\nSelecciona el rol del usuario:")
    for indice, rol in enumerate(disponibles, start=1):
        print(f"{indice}. {rol.nombre_rol}")
    try:
        rol = disponibles[int(leer_opcion("Rol: ")) - 1]
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
        id_rol=rol.id_rol,
    )
    if usuario is None:
        print("No se pudo crear el usuario: el nombre o correo ya existe.")
        return
    print(f"Usuario creado correctamente. Tu ID es: {usuario.id_usuario}")


def procesar_compra_curso(usuario: Usuario, datos: dict[str, object]) -> None:
    cursos = datos["cursos"]
    disponibles = cursos.listar()
    cursos.mostrar_cursos()
    if not disponibles:
        return
    try:
        curso = disponibles[
            int(leer_opcion("Selecciona el número del curso a comprar: ")) - 1
        ]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return
    if any(
        registro.id_usuario == usuario.id_usuario
        and registro.id_curso == curso.id_curso
        for registro in datos["inscripciones"].listar()
    ):
        print(f"Ya adquiriste '{curso.nombre}' anteriormente.")
        return

    print(f"\nCurso: {curso.nombre}\nPrecio: ${curso.precio:.2f}")
    metodo = (
        leer_opcion("Método de pago (tarjeta/transferencia/efectivo): ").lower()
        or "efectivo"
    )
    referencia = (
        leer_opcion("Número de tarjeta (13 a 19 dígitos): ")
        if metodo == "tarjeta"
        else None
    )
    ok, mensaje = datos["pagos"].validar_pago(metodo, referencia)
    if not ok:
        print(mensaje)
        return
    print(mensaje)

    factura = datos["facturas"].crear(
        Factura(
            numero_factura="",
            total=curso.precio,
            id_usuario=usuario.id_usuario,
            id_curso=curso.id_curso,
            metodo_pago=metodo,
            estado="pagada",
        )
    )
    pago = datos["pagos"].crear(
        datos["pagos"].crear_pago(
            monto=curso.precio,
            metodo_pago=metodo,
            id_usuario=usuario.id_usuario,
            id_curso=curso.id_curso,
            id_factura=factura.id_factura,
        )
    )
    inscripcion = datos["inscripciones"].crear(
        Inscripcion(
            id_usuario=usuario.id_usuario, id_curso=curso.id_curso, estado="activa"
        )
    )
    datos["progresos"].crear(
        Progreso(
            id_usuario=usuario.id_usuario, id_curso=curso.id_curso, estado="En progreso"
        )
    )
    print(
        datos["facturas"].generar_comprobante(
            factura, curso.nombre, nombre_completo(usuario)
        )
    )
    print(f"ID de inscripción: {inscripcion.id_inscripcion}")
    print(f"Estado del pago: {pago.estado}\nCompra realizada con éxito.")


def mostrar_historial_pagos(usuario: Usuario, datos: dict[str, object]) -> None:
    pagos = [
        pago
        for pago in datos["pagos"].listar()
        if pago.id_usuario == usuario.id_usuario
    ]
    if not pagos:
        print("Todavía no tienes pagos registrados.")
        return
    print("\nHistorial de pagos:")
    for pago in pagos:
        print(f"- {datos['pagos'].resumen(pago)}")


def gestionar_resenas(usuario: Usuario, datos: dict[str, object]) -> None:
    inscripciones = [
        inscripcion
        for inscripcion in datos["inscripciones"].listar()
        if inscripcion.id_usuario == usuario.id_usuario
    ]
    cursos_aprobados = []
    for inscripcion in inscripciones:
        progreso = next(
            (
                registro
                for registro in datos["progresos"].listar()
                if registro.id_usuario == usuario.id_usuario
                and registro.id_curso == inscripcion.id_curso
                and registro.id_leccion is None
                and registro.porcentaje >= 100
                and registro.estado.casefold() == "completado"
            ),
            None,
        )
        curso = datos["cursos"].obtener(inscripcion.id_curso)
        if progreso is not None and curso is not None:
            cursos_aprobados.append(curso)

    if not cursos_aprobados:
        print("No tienes cursos aprobados para reseñar.")
        return

    print("\nCursos aprobados:")
    for indice, curso in enumerate(cursos_aprobados, start=1):
        resena = datos["resenas"].obtener_por_usuario_curso(
            usuario.id_usuario, curso.id_curso
        )
        estado = "con reseña" if resena is not None else "sin reseña"
        print(f"{indice}. {curso.nombre} - {estado}")

    try:
        curso = cursos_aprobados[int(leer_opcion("Selecciona el curso: ")) - 1]
        calificacion = int(leer_opcion("Calificación (1 a 5): "))
    except (ValueError, IndexError):
        print("Selección o calificación inválida.")
        return
    if not 1 <= calificacion <= 5:
        print("La calificación debe estar entre 1 y 5.")
        return

    comentario = leer_opcion("Comentario: ")
    resena = datos["resenas"].obtener_por_usuario_curso(
        usuario.id_usuario, curso.id_curso
    )
    if resena is None:
        datos["resenas"].crear(
            calificacion=calificacion,
            comentario=comentario,
            id_usuario=usuario.id_usuario,
            id_curso=curso.id_curso,
        )
        print("Reseña guardada en la base de datos.")
    else:
        datos["resenas"].actualizar(resena.id_resena, calificacion, comentario)
        print("Reseña actualizada en la base de datos.")


def curso_tiene_evaluaciones_respondidas(
    usuario: Usuario, id_curso: UUID, datos: dict[str, object]
) -> bool:
    modulos = [m for m in datos["modulos"].listar() if m.id_curso == id_curso]
    lecciones = [
        leccion
        for leccion in datos["lecciones"].listar()
        if any(leccion.id_modulo == modulo.id_modulo for modulo in modulos)
    ]
    respondidas = {
        evaluacion.id_leccion
        for evaluacion in datos["evaluaciones"].listar()
        if evaluacion.id_usuario == usuario.id_usuario and evaluacion.calificacion > 0
    }
    return bool(lecciones) and all(
        leccion.id_leccion in respondidas for leccion in lecciones
    )


def resolver_evaluacion_leccion(
    usuario: Usuario, leccion, datos: dict[str, object]
) -> bool:
    disenos = [
        evaluacion
        for evaluacion in datos["evaluaciones"].listar()
        if evaluacion.id_leccion == leccion.id_leccion
        and evaluacion.id_usuario != usuario.id_usuario
    ]
    if not disenos:
        print("Esta lección no tiene una evaluación diseñada por el profesor.")
        return False
    diseno = disenos[0]
    print(f"\nEvaluación: {diseno.nombre}\nDescripción: {diseno.descripcion}")
    respuesta = next(
        (
            evaluacion
            for evaluacion in datos["evaluaciones"].listar()
            if evaluacion.id_leccion == leccion.id_leccion
            and evaluacion.id_usuario == usuario.id_usuario
        ),
        None,
    )
    if respuesta is not None and respuesta.calificacion > 0:
        print(f"Evaluación respondida. Calificación: {respuesta.calificacion:.2f}/100")
        return True
    try:
        calificacion = float(leer_opcion("Calificación obtenida (0 a 100): "))
    except ValueError:
        print("La calificación debe ser un número.")
        return False
    if not 0 <= calificacion <= 100:
        print("La calificación debe estar entre 0 y 100.")
        return False
    if respuesta is None:
        datos["evaluaciones"].crear(
            Evaluacion(
                nombre=diseno.nombre,
                descripcion=diseno.descripcion,
                calificacion=calificacion,
                id_leccion=leccion.id_leccion,
                id_usuario=usuario.id_usuario,
            )
        )
    else:
        datos["evaluaciones"].actualizar(
            respuesta.id_evaluacion, {"calificacion": calificacion}
        )
    print("Evaluación guardada en la base de datos.")
    return calificacion > 0


def completar_curso(usuario: Usuario, datos: dict[str, object]) -> None:
    inscripciones = [
        i for i in datos["inscripciones"].listar() if i.id_usuario == usuario.id_usuario
    ]
    if not inscripciones:
        print("No tienes cursos inscritos.")
        return
    print("\nCursos inscritos:")
    for indice, inscripcion in enumerate(inscripciones, start=1):
        print(f"{indice}. {datos['cursos'].obtener(inscripcion.id_curso).nombre}")
    try:
        inscripcion = inscripciones[
            int(leer_opcion("Selecciona el curso que deseas culminar: ")) - 1
        ]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    curso = datos["cursos"].obtener(inscripcion.id_curso)
    modulos = [m for m in datos["modulos"].listar() if m.id_curso == curso.id_curso]
    lecciones = [
        leccion
        for leccion in datos["lecciones"].listar()
        if any(leccion.id_modulo == modulo.id_modulo for modulo in modulos)
    ]
    lecciones.sort(key=lambda leccion: (leccion.id_modulo, leccion.orden))
    if not lecciones:
        print("Este curso todavía no tiene lecciones disponibles.")
        return
    vistos = {
        progreso.id_leccion
        for progreso in datos["progresos"].listar()
        if progreso.id_usuario == usuario.id_usuario
        and progreso.id_curso == curso.id_curso
        and progreso.id_leccion is not None
        and progreso.porcentaje >= 100
    }
    print(f"\nLecciones de '{curso.nombre}':")
    for indice, leccion in enumerate(lecciones, start=1):
        print(
            f"{indice}. {leccion.nombre} ({leccion.duracion} min) - {'vista' if leccion.id_leccion in vistos else 'pendiente'}"
        )
    try:
        leccion = lecciones[
            int(leer_opcion("Selecciona la lección que deseas ver: ")) - 1
        ]
    except (ValueError, IndexError):
        print("Selección de lección inválida.")
        return
    print(
        f"\n--- {leccion.nombre} ---\n{leccion.contenido}\nDuración estimada: {leccion.duracion} minutos"
    )
    if not resolver_evaluacion_leccion(usuario, leccion, datos):
        print("Debes completar la evaluación para avanzar en esta lección.")
        return
    if leccion.id_leccion not in vistos:
        if leer_opcion("¿Marcar esta lección como vista? (s/n): ").lower() != "s":
            print("La lección no se marcó como vista.")
            return
        datos["progresos"].crear(
            Progreso(
                id_usuario=usuario.id_usuario,
                id_curso=curso.id_curso,
                id_leccion=leccion.id_leccion,
                porcentaje=100.0,
                estado="Completado",
            )
        )
        vistos.add(leccion.id_leccion)
        print("Lección marcada como vista y guardada en la base de datos.")

    porcentaje = round(len(vistos) * 100 / len(lecciones), 2)
    resumen = next(
        (
            progreso
            for progreso in datos["progresos"].listar()
            if progreso.id_usuario == usuario.id_usuario
            and progreso.id_curso == curso.id_curso
            and progreso.id_leccion is None
        ),
        None,
    )
    cambios = {
        "porcentaje": porcentaje,
        "estado": "Completado" if porcentaje >= 100 else "En progreso",
    }
    if resumen is None:
        datos["progresos"].crear(
            Progreso(id_usuario=usuario.id_usuario, id_curso=curso.id_curso, **cambios)
        )
    else:
        datos["progresos"].actualizar(resumen.id_progreso, cambios)
    print(
        f"Progreso de '{curso.nombre}': {porcentaje:.2f}% ({len(vistos)}/{len(lecciones)} lecciones)"
    )
    if porcentaje < 100 or not curso_tiene_evaluaciones_respondidas(
        usuario, curso.id_curso, datos
    ):
        if porcentaje >= 100:
            print("Debes completar las evaluaciones de todas las lecciones.")
        return

    certs = datos["certificados"]
    if certs.obtener_por_usuario_curso(usuario.id_usuario, curso.id_curso) is not None:
        print("El certificado de este curso ya está guardado en la base de datos.")
        return
    certificado = certs.emitir_si_aplica(
        pagos=list(datos["pagos"].listar()),
        facturas=list(datos["facturas"].listar()),
        progresos=list(datos["progresos"].listar()),
        id_usuario=usuario.id_usuario,
        id_curso=curso.id_curso,
    )
    if certificado is not None:
        certs.crear(certificado)
        print(f"Certificado emitido: {certificado.codigo}")


def sincronizar_certificados(usuario: Usuario, datos: dict[str, object]) -> None:
    certs = datos["certificados"]
    for inscripcion in datos["inscripciones"].listar():
        if (
            inscripcion.id_usuario != usuario.id_usuario
            or certs.obtener_por_usuario_curso(usuario.id_usuario, inscripcion.id_curso)
        ):
            continue
        if not curso_tiene_evaluaciones_respondidas(
            usuario, inscripcion.id_curso, datos
        ):
            continue
        factura = next(
            (
                f
                for f in datos["facturas"].listar()
                if f.id_usuario == usuario.id_usuario
                and f.id_curso == inscripcion.id_curso
            ),
            None,
        )
        pago = next(
            (
                p
                for p in datos["pagos"].listar()
                if p.id_usuario == usuario.id_usuario
                and p.id_curso == inscripcion.id_curso
                and p.estado == "pagado"
            ),
            None,
        )
        if factura and pago and factura.estado == "emitida":
            datos["facturas"].actualizar(factura.id_factura, {"estado": "pagada"})
        certificado = certs.emitir_si_aplica(
            pagos=list(datos["pagos"].listar()),
            facturas=list(datos["facturas"].listar()),
            progresos=list(datos["progresos"].listar()),
            id_usuario=usuario.id_usuario,
            id_curso=inscripcion.id_curso,
            mostrar_mensaje=False,
        )
        if certificado:
            certs.crear(certificado)


def mostrar_certificados(usuario: Usuario, datos: dict[str, object]) -> None:
    sincronizar_certificados(usuario, datos)
    certificados = [
        c for c in datos["certificados"].listar() if c.id_usuario == usuario.id_usuario
    ]
    if not certificados:
        print("Todavía no tienes certificados emitidos.")
        return
    print("\nCertificados emitidos:")
    for certificado in certificados:
        curso = datos["cursos"].obtener(certificado.id_curso)
        print(
            f"- {curso.nombre if curso else 'Curso desconocido'} | {certificado.codigo} | {certificado.fecha_emision:%d/%m/%Y}"
        )


def crear_evaluacion_profesor(usuario: Usuario, datos: dict[str, object]) -> None:
    cursos = datos["modulos"].cursos_del_instructor(usuario, datos)
    if not cursos:
        print("No tienes cursos asignados para crear evaluaciones.")
        return
    print("\nTus cursos asignados:")
    for indice, curso in enumerate(cursos, start=1):
        print(f"{indice}. {curso.nombre}")
    try:
        curso = cursos[int(leer_opcion("Selecciona el curso: ")) - 1]
    except (ValueError, IndexError):
        print("Selección de curso inválida.")
        return
    modulos = [m for m in datos["modulos"].listar() if m.id_curso == curso.id_curso]
    if not modulos:
        print(f"El curso '{curso.nombre}' no tiene módulos asociados.")
        return
    print(f"\nMódulos de '{curso.nombre}':")
    for indice, modulo in enumerate(modulos, start=1):
        print(f"{indice}. {modulo.nombre}")
    try:
        modulo = modulos[int(leer_opcion("Selecciona el módulo: ")) - 1]
    except (ValueError, IndexError):
        print("Selección de módulo inválida.")
        return
    lecciones = sorted(
        [l for l in datos["lecciones"].listar() if l.id_modulo == modulo.id_modulo],
        key=lambda leccion: leccion.orden,
    )
    if not lecciones:
        print(f"El módulo '{modulo.nombre}' no tiene lecciones.")
        return
    print(f"\nLecciones de '{modulo.nombre}':")
    for indice, leccion in enumerate(lecciones, start=1):
        print(f"{indice}. {leccion.nombre}")
    try:
        leccion = lecciones[int(leer_opcion("Selecciona la lección: ")) - 1]
    except (ValueError, IndexError):
        print("Selección de lección inválida.")
        return
    evaluacion = datos["evaluaciones"].crear(
        Evaluacion(
            nombre=leer_opcion("Nombre de la evaluación: "),
            descripcion=leer_opcion("Descripción de la evaluación: "),
            calificacion=0.0,
            id_leccion=leccion.id_leccion,
            id_usuario=usuario.id_usuario,
        )
    )
    print(
        f"Evaluación creada correctamente: {evaluacion.nombre}"
        f" | ID: {evaluacion.id_evaluacion}"
    )


def crear_resena_ejemplo(
    usuario: Usuario, id_curso: UUID, datos: dict[str, object]
) -> None:
    resenas: ResenaCRUD = datos["resenas"]
    resenas.crear(
        calificacion=int(leer_opcion("Calificación (1 a 5): ")),
        comentario=leer_opcion("Comentario: "),
        id_usuario=usuario.id_usuario,
        id_curso=id_curso,
    )
    print("¡Reseña publicada con éxito!")
