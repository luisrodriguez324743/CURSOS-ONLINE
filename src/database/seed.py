from uuid import UUID
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.database.init_db import init_db 
from src.entities.rol import Rol
from src.entities.curso import Curso
from src.entities.modulo import Modulo
from src.entities.leccion import Leccion
from src.entities.certificado import Certificado

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
        print("Cargando datos iniciales...")
        
        # 🟢 Ejecución ordenada respetando la integridad referencial (FK)
        _seed_roles(session)
        _seed_cursos(session)
        _seed_modulos(session)
        _seed_certificados(session)
        _seed_lecciones(session)

        session.commit()
        print("¡Datos cargados exitosamente!")
    except Exception as err:
        session.rollback()
        print(f"Error al ejecutar seed: {err}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()