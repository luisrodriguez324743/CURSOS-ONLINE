import sys
from pathlib import Path

# Registramos la raíz del proyecto (CURSOS_ONLINE) en el PATH de Python
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uuid
from datetime import date
from src.database.connection import get_session

# --- IMPORTACIONES DESDE LA CARPETA 'entities' ---
from src.entities.rol import Rol
from src.entities.usuario import Usuario
from src.entities.resena import Resena
# from src.entities.curso import Curso  # Comentado hasta que tu compañero cree la entidad


def seed_data():
    session = get_session()
    try:
        print("🌱 Iniciando el proceso de seeding en Neon DB...")

        # -------------------------------------------------------------
        # 1. POBLAR ROLES
        # -------------------------------------------------------------
        roles_data = [
            {"nombre_rol": "Administrador", "descripcion": "Control total del sistema"},
            {"nombre_rol": "Instructor", "descripcion": "Creador de contenido y cursos"},
            {"nombre_rol": "Estudiante", "descripcion": "Usuario consumidor de cursos"},
        ]

        roles_creados = {}
        for r_data in roles_data:
            rol = session.query(Rol).filter_by(nombre_rol=r_data["nombre_rol"]).first()
            if not rol:
                rol = Rol(
                    id_rol=uuid.uuid4(),
                    nombre_rol=r_data["nombre_rol"],
                    descripcion=r_data["descripcion"]
                )
                session.add(rol)
                print(f"  [+] Rol creado: {rol.nombre_rol}")
            else:
                print(f"  [-] Rol ya existente: {rol.nombre_rol}")
            
            roles_creados[r_data["nombre_rol"]] = rol

        session.commit()

        # -------------------------------------------------------------
        # 2. POBLAR USUARIOS
        # -------------------------------------------------------------
        usuarios_data = [
            {
                "primer_nombre": "Carlos",
                "primer_apellido": "Gómez",
                "nombre_usuario": "admin_carlos",
                "correo": "carlos.admin@email.com",
                "clave": "admin123",
                "area": "Sistemas",
                "rol": roles_creados["Administrador"]
            },
            {
                "primer_nombre": "María",
                "primer_apellido": "López",
                "nombre_usuario": "prof_maria",
                "correo": "maria.prof@email.com",
                "clave": "prof123",
                "area": "Desarrollo Web",
                "rol": roles_creados["Instructor"]
            },
            {
                "primer_nombre": "Juan",
                "primer_apellido": "Pérez",
                "nombre_usuario": "juan_perez",
                "correo": "juan.perez@email.com",
                "clave": "juan123",
                "area": "Estudiante",
                "rol": roles_creados["Estudiante"]
            }
        ]

        usuarios_creados = []
        for u_data in usuarios_data:
            usuario = session.query(Usuario).filter_by(nombre_usuario=u_data["nombre_usuario"]).first()
            if not usuario:
                usuario = Usuario(
                    id_usuario=uuid.uuid4(),
                    primer_nombre=u_data["primer_nombre"],
                    primer_apellido=u_data["primer_apellido"],
                    nombre_usuario=u_data["nombre_usuario"],
                    correo=u_data["correo"],
                    clave=u_data["clave"],
                    area=u_data["area"],
                    id_rol=u_data["rol"].id_rol,
                    activo=True,
                    fecha_creacion=date.today()
                )
                session.add(usuario)
                print(f"  [+] Usuario creado: {usuario.nombre_usuario}")
            else:
                print(f"  [-] Usuario ya existente: {usuario.nombre_usuario}")
            
            usuarios_creados.append(usuario)

        session.commit()

        # -------------------------------------------------------------
        # 3. POBLAR RESEÑAS
        # -------------------------------------------------------------
        estudiante = next((u for u in usuarios_creados if u.nombre_usuario == "juan_perez"), None)

        if estudiante:
            id_curso_ficticio = uuid.uuid4()

            resena_existente = session.query(Resena).filter_by(
                id_usuario=estudiante.id_usuario
            ).first()

            if not resena_existente:
                resena = Resena(
                    id_resena=uuid.uuid4(),
                    calificacion=5,
                    comentario="¡Excelente curso! Muy bien explicado.",
                    id_usuario=estudiante.id_usuario,
                    id_curso=id_curso_ficticio,
                    fecha_creacion=date.today()
                )
                session.add(resena)
                session.commit()
                print(f"  [+] Reseña creada con éxito para el usuario {estudiante.nombre_usuario}")
            else:
                print("  [-] La reseña de prueba ya existe.")

        print("🚀 ¡Seeding completado con éxito!")

    except Exception as e:
        session.rollback()
        print(f"❌ Error durante el seeding: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()