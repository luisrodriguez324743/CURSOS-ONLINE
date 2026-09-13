from sqlalchemy import text
from src.database.connection import SessionLocal

# Lista de tablas en plural que deseas eliminar
TABLAS_PLURAL = [
    "certificados",
    "evaluaciones",
    "facturas",
    "inscripciones",
    "lecciones",
    "modulos",
    "pagos",
    "progresos",
    "resenas",
    "roles",
    "usuarios",
    "cursos",
]

def eliminar_tablas_plural():
    db = SessionLocal()
    try:
        print("Eliminando tablas en plural...")
        for tabla in TABLAS_PLURAL:
            # CASCADE fuerza el borrado eliminando también las restricciones de clave foránea vinculadas
            sql = text(f'DROP TABLE IF EXISTS "public"."{tabla}" CASCADE;')
            db.execute(sql)
            print(f"✓ Tabla '{tabla}' eliminada (si existía).")
        
        db.commit()
        print("\n¡Proceso completado con éxito! Las tablas en plural han sido eliminadas.")
    except Exception as e:
        db.rollback()
        print(f"\nError al intentar borrar las tablas: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    eliminar_tablas_plural()