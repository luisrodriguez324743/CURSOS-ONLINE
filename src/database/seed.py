from uuid import UUID
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.database.init_db import init_db 
from src.entities.rol import Rol
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.pago import Pago
from src.entities.progreso import Progreso
from src.entities.resena import Resena
from src.entities.rol import Rol
from src.entities.usuario import Usuario
from src.entities.evaluacion import Evaluacion

ROL_INSTRUCTOR_ID = UUID("10000000-0000-0000-0000-000000000001")
ROL_ESTUDIANTE_ID = UUID("10000000-0000-0000-0000-000000000002")
INSTRUCTOR_ID = UUID("20000000-0000-0000-0000-000000000001")
ESTUDIANTE_ID = UUID("20000000-0000-0000-0000-000000000002")
CURSO_ID = UUID("30000000-0000-0000-0000-000000000001")
MODULO_ID = UUID("40000000-0000-0000-0000-000000000001")
LECCION_ID = UUID("50000000-0000-0000-0000-000000000001")
RESENA_ID = UUID("60000000-0000-0000-0000-000000000001")
FACTURA_ID = UUID("70000000-0000-0000-0000-000000000001")
PAGO_ID = UUID("80000000-0000-0000-0000-000000000001")
CERTIFICADO_ID = UUID("90000000-0000-0000-0000-000000000001")
INSCRIPCION_ID = UUID("a0000000-0000-0000-0000-000000000001")
PROGRESO_ID = UUID("b0000000-0000-0000-0000-000000000001")
EVALUACION_ID = UUID("c0000000-0000-0000-0000-000000000001")
PROGRESO_RESUMEN_ID = UUID("b0000000-0000-0000-0000-000000000002")
EVALUACION_PROFESOR_ID = UUID("c0000000-0000-0000-0000-000000000002")


def _add_if_missing(session, model, identificador, **values):
    registro = session.get(model, identificador)
    if registro is not None:
        return registro
    registro = model(**values)
    session.add(registro)
    session.flush()
    return registro


def _add_by_unique_field(session, model, field_name, field_value, **values):
    registro = session.query(model).filter_by(**{field_name: field_value}).first()
    if registro is not None:
        return registro
    registro = model(**values)
    session.add(registro)
    session.flush()
    return registro


def _seed_roles(session) -> tuple[UUID, UUID]:
    instructor_role = _add_by_unique_field(
        session,
        Rol,
        "nombre_rol",
        "Instructor",
        id_rol=ROL_INSTRUCTOR_ID,
        nombre_rol="Instructor",
        descripcion="Usuario que crea y administra cursos.",
    )
    student_role = _add_by_unique_field(
        session,
        Rol,
        "nombre_rol",
        "Estudiante",
        id_rol=ROL_ESTUDIANTE_ID,
        nombre_rol="Estudiante",
        descripcion="Usuario que se inscribe en cursos.",
    )
    return instructor_role.id_rol, student_role.id_rol


def _seed_usuarios(session, instructor_role_id: UUID, student_role_id: UUID):
    instructor = _add_by_unique_field(
        session,
        Usuario,
        "nombre_usuario",
        "instructor_demo",
        id_usuario=INSTRUCTOR_ID,
        primer_nombre="Ana",
        segundo_nombre="",
        primer_apellido="García",
        segundo_apellido="López",
        nombre_usuario="instructor_demo",
        correo="instructor.demo@cursos.local",
        clave="demo123",
        area="Tecnología",
        id_rol=instructor_role_id,
    )
    student = _add_by_unique_field(
        session,
        Usuario,
        "nombre_usuario",
        "estudiante_demo",
        id_usuario=ESTUDIANTE_ID,
        primer_nombre="Carlos",
        segundo_nombre="",
        primer_apellido="Pérez",
        segundo_apellido="Ruiz",
        nombre_usuario="estudiante_demo",
        correo="estudiante.demo@cursos.local",
        clave="demo123",
        area="Desarrollo",
        id_rol=student_role_id,
    )
    return instructor.id_usuario, student.id_usuario


def _seed_curso_y_contenido(session, instructor_id: UUID) -> None:
    _add_if_missing(
        session,
        Curso,
        CURSO_ID,
        id_curso=CURSO_ID,
        nombre="Python desde cero",
        descripcion="Fundamentos del lenguaje Python.",
        precio=25.0,
        id_profesor=instructor_id,
    )
    _add_if_missing(
        session,
        Modulo,
        MODULO_ID,
        id_modulo=MODULO_ID,
        nombre="Fundamentos",
        descripcion="Conceptos básicos de Python.",
        orden=1,
        id_curso=CURSO_ID,
    )
    _add_if_missing(
        session,
        Leccion,
        LECCION_ID,
        id_leccion=LECCION_ID,
        nombre="Variables y tipos de datos",
        contenido="Tipos básicos, variables y operaciones en Python.",
        orden=1,
        duracion=30,
        id_modulo=MODULO_ID,
    )


def _seed_resena(session, student_id: UUID) -> None:
    _add_if_missing(
        session,
        Resena,
        RESENA_ID,
        id_resena=RESENA_ID,
        calificacion=5,
        comentario="Curso claro y práctico.",
        id_usuario=student_id,
        id_curso=CURSO_ID,
    )


def _seed_factura_pago_certificado(
    session, student_id: UUID, inscription_id: UUID
) -> None:
    factura = _add_if_missing(
        session,
        Factura,
        FACTURA_ID,
        id_factura=FACTURA_ID,
        numero_factura="FAC-DEMO-001",
        total=25.0,
        id_inscripcion=inscription_id,
        id_usuario=student_id,
        id_curso=CURSO_ID,
        metodo_pago="tarjeta",
        estado="pagada",
    )
    if factura.id_inscripcion is None:
        factura.id_inscripcion = inscription_id
        session.flush()

    _add_if_missing(
        session,
        Pago,
        PAGO_ID,
        id_pago=PAGO_ID,
        monto=25.0,
        metodo_pago="tarjeta",
        estado="pagado",
        id_usuario=student_id,
        id_curso=CURSO_ID,
        id_factura=FACTURA_ID,
    )
    _add_if_missing(
        session,
        Certificado,
        CERTIFICADO_ID,
        id_certificado=CERTIFICADO_ID,
        codigo="CERT-DEMO-001",
        id_usuario=student_id,
        id_curso=CURSO_ID,
    )


def _seed_academico(session, instructor_id: UUID, student_id: UUID) -> UUID:
    inscripcion = _add_if_missing(
        session,
        Inscripcion,
        INSCRIPCION_ID,
        id_inscripcion=INSCRIPCION_ID,
        estado="activa",
        id_usuario=student_id,
        id_curso=CURSO_ID,
    )
    _add_if_missing(
        session,
        Progreso,
        PROGRESO_ID,
        id_progreso=PROGRESO_ID,
        porcentaje=100.0,
        estado="Completado",
        id_usuario=student_id,
        id_curso=CURSO_ID,
        id_leccion=LECCION_ID,
    )
    _add_if_missing(
        session,
        Progreso,
        PROGRESO_RESUMEN_ID,
        id_progreso=PROGRESO_RESUMEN_ID,
        porcentaje=100.0,
        estado="Completado",
        id_usuario=student_id,
        id_curso=CURSO_ID,
        id_leccion=None,
    )
    _add_if_missing(
        session,
        Evaluacion,
        EVALUACION_PROFESOR_ID,
        id_evaluacion=EVALUACION_PROFESOR_ID,
        nombre="Evaluación de fundamentos",
        descripcion="Identifica variables y tipos de datos de Python.",
        calificacion=0.0,
        id_leccion=LECCION_ID,
        id_usuario=instructor_id,
    )
    _add_if_missing(
        session,
        Evaluacion,
        EVALUACION_ID,
        id_evaluacion=EVALUACION_ID,
        nombre="Evaluación de fundamentos",
        descripcion="Evaluación inicial del curso.",
        calificacion=95.0,
        id_leccion=LECCION_ID,
        id_usuario=student_id,
    )
    return inscripcion.id_inscripcion


def _seed_evaluacion_por_curso(session) -> None:
    cursos = session.query(Curso).all()
    for curso in cursos:
        leccion = (
            session.query(Leccion)
            .join(Modulo, Leccion.id_modulo == Modulo.id_modulo)
            .filter(Modulo.id_curso == curso.id_curso)
            .order_by(Modulo.orden, Leccion.orden)
            .first()
        )
        if leccion is None:
            continue

        evaluacion = (
            session.query(Evaluacion).filter_by(id_leccion=leccion.id_leccion).first()
        )
        if evaluacion is not None:
            continue

        _add_if_missing(
            session,
            Evaluacion,
            uuid4(),
            nombre=f"Evaluación de {curso.nombre}",
            descripcion=f"Evaluación general del curso {curso.nombre}.",
            calificacion=0.0,
            id_leccion=leccion.id_leccion,
            id_usuario=curso.id_profesor,
        )

# =====================================================================
# 1. IDENTIFICADORES ÚNICOS (UUIDs Fijos)
# =====================================================================
# Roles
ROL_ADMIN_ID = UUID("10000000-0000-0000-0000-000000000001")
ROL_INSTRUCTOR_ID = UUID("10000000-0000-0000-0000-000000000002")
ROL_ENCARGADO_ID = UUID("10000000-0000-0000-0000-000000000003")
ROL_ESTUDIANTE_ID = UUID("10000000-0000-0000-0000-000000000004")

# Cursos
CURSO_JAVA_ID = UUID("30000000-0000-0000-0000-000000000001")
CURSO_PYTHON_ID = UUID("30000000-0000-0000-0000-000000000002")
CURSO_INGLES_ID = UUID("30000000-0000-0000-0000-000000000003")
CURSO_SQL_ID = UUID("30000000-0000-0000-0000-000000000004")

# Módulos
MODULO_JAVA_ID = UUID("40000000-0000-0000-0000-000000000001")
MODULO_PYTHON_ID = UUID("40000000-0000-0000-0000-000000000002")
MODULO_INGLES_ID = UUID("40000000-0000-0000-0000-000000000003")
MODULO_SQL_ID = UUID("40000000-0000-0000-0000-000000000004")


# =====================================================================
# 2. FUNCIONES DE CARGA MANUAL
# =====================================================================

def _seed_roles(session) -> None:
    roles = [
        {"id_rol": ROL_ADMIN_ID, "nombre_rol": "Administrador", "descripcion": "Control total del sistema."},
        {"id_rol": ROL_INSTRUCTOR_ID, "nombre_rol": "Instructor", "descripcion": "Imparte y gestiona contenidos."},
        {"id_rol": ROL_ENCARGADO_ID, "nombre_rol": "Encargado de curso", "descripcion": "Supervisa cursos asignados."},
        {"id_rol": ROL_ESTUDIANTE_ID, "nombre_rol": "Estudiante", "descripcion": "Accede a cursos e inscripciones."},
    ]
    for datos in roles:
        if not session.query(Rol).filter_by(nombre_rol=datos["nombre_rol"]).first():
            session.add(Rol(**datos))


def _seed_cursos(session) -> None:
    cursos = [
        {
            "id_curso": CURSO_JAVA_ID,
            "nombre": "Java Profesional",
            "descripcion": "Aprende Java desde cero hasta desarrollo Backend con Spring Boot.",
            "precio": 50.0,
        },
        {
            "id_curso": CURSO_PYTHON_ID,
            "nombre": "Python desde Cero",
            "descripcion": "Fundamentos de Python, ciencia de datos y desarrollo con FastAPI.",
            "precio": 45.0,
        },
        {
            "id_curso": CURSO_INGLES_ID,
            "nombre": "Inglés Técnico para Desarrolladores",
            "descripcion": "Vocabulario y comunicación para trabajar en tecnología.",
            "precio": 30.0,
        },
        {
            "id_curso": CURSO_SQL_ID,
            "nombre": "SQL para Desarrolladores",
            "descripcion": "Aprende SQL desde los fundamentos hasta consultas avanzadas.",
            "precio": 40.0,
        },
    ]
    for datos in cursos:
        if not session.get(Curso, datos["id_curso"]):
            session.add(Curso(**datos))


# 🟢 AQUÍ VA TU LISTA DE MÓDULOS EN SU PROPIA FUNCIÓN
def _seed_modulos(session) -> None:
    modulos = [
        {
            "id_modulo": MODULO_JAVA_ID,
            "nombre": "Módulo 1: Fundamentos de Java",
            "id_curso": CURSO_JAVA_ID
        },
        {
            "id_modulo": MODULO_PYTHON_ID,
            "nombre": "Módulo 1: Fundamentos de Python",
            "id_curso": CURSO_PYTHON_ID
        },
        {
            "id_modulo": MODULO_INGLES_ID,
            "nombre": "Módulo 1: Inglés Técnico",
            "id_curso": CURSO_INGLES_ID
        },
        {
            "id_modulo": MODULO_SQL_ID,
            "nombre": "Módulo 1: Consultas Básicas SQL",
            "id_curso": CURSO_SQL_ID
        },
    ]
    for datos in modulos:
        if not session.get(Modulo, datos["id_modulo"]):
            session.add(Modulo(**datos))


def _seed_certificados(session) -> None:
    certificados = [
        {"codigo": "CERT-JAVA-2026", "id_curso": CURSO_JAVA_ID},
        {"codigo": "CERT-PYTHON-2026", "id_curso": CURSO_PYTHON_ID},
        {"codigo": "CERT-INGLES-2026", "id_curso": CURSO_INGLES_ID},
        {"codigo": "CERT-SQL-2026", "id_curso": CURSO_SQL_ID},
    ]
    for datos in certificados:
        if not session.query(Certificado).filter_by(codigo=datos["codigo"]).first():
            session.add(Certificado(**datos))


def _seed_lecciones(session) -> None:
    lecciones = [
        {
            "nombre": "Introducción a la JVM y Sintaxis Java",
            "contenido": "Variables, tipos de datos y compilación.",
            "orden": 1,
            "duracion": 15,
            "id_modulo": MODULO_JAVA_ID,  # 🟢 Cambiado a id_modulo
        },
        {
            "nombre": "Sintaxis Básica de Python",
            "contenido": "Tipos dinámicos, listas y diccionarios.",
            "orden": 1,
            "duracion": 20,
            "id_modulo": MODULO_PYTHON_ID,
        },
        {
            "nombre": "Vocabulario en Entrevistas Técnicas",
            "contenido": "Cómo presentar tus proyectos en inglés.",
            "orden": 1,
            "duracion": 30,
            "id_modulo": MODULO_INGLES_ID,
        },
        {
            "nombre": "Fundamentos de SQL",
            "contenido": "Consultas básicas y manipulación de datos.",
            "orden": 1,
            "duracion": 25,
            "id_modulo": MODULO_SQL_ID,
        },
    ]
    for datos in lecciones:
        if not session.query(Leccion).filter_by(nombre=datos["nombre"], id_modulo=datos["id_modulo"]).first():
            session.add(Leccion(**datos))


# =====================================================================
# 3. EJECUCIÓN PRINCIPAL
# =====================================================================

def seed() -> None:
    init_db()
    
    session = SessionLocal()
    try:
        instructor_role_id, student_role_id = _seed_roles(session)
        instructor_id, student_id = _seed_usuarios(
            session, instructor_role_id, student_role_id
        )
        _seed_curso_y_contenido(session, instructor_id)
        _seed_resena(session, student_id)
        inscription_id = _seed_academico(session, instructor_id, student_id)
        _seed_factura_pago_certificado(session, student_id, inscription_id)
        _seed_evaluacion_por_curso(session)
        session.commit()
        print("¡Datos cargados exitosamente!")
    except Exception as err:
        session.rollback()
        print(f"Error al ejecutar seed: {err}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()