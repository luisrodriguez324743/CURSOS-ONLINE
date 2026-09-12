from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError

from src.database.connection import Base, SessionLocal, engine
from src.database.schema import remove_empty_legacy_tables
from src.entities.certificado import Certificado
from src.entities.curso import Curso
from src.entities.factura import Factura
from src.entities.inscripcion import Inscripcion
from src.entities.leccion import Leccion
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


def seed() -> None:
    remove_empty_legacy_tables()
    Base.metadata.create_all(bind=engine)
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
        print("Datos semilla cargados correctamente.")
        print(
            "Registros: "
            f"inscripciones={session.query(Inscripcion).count()}, "
            f"progresos={session.query(Progreso).count()}, "
            f"evaluaciones={session.query(Evaluacion).count()}"
        )
    except IntegrityError:
        session.rollback()
        print(
            "No se pudieron cargar los datos semilla por una restricción de integridad."
        )
    finally:
        session.close()


if __name__ == "__main__":
    seed()
