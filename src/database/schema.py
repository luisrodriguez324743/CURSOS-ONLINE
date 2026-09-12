from sqlalchemy import inspect, text

from src.database.connection import engine

LEGACY_TABLES = ("inscripcion", "progreso", "evaluacion")


def remove_empty_legacy_tables() -> None:
    inspector = inspect(engine)
    tablas = set(inspector.get_table_names())
    if not tablas.intersection(LEGACY_TABLES):
        return

    with engine.begin() as connection:
        for tabla in LEGACY_TABLES:
            if tabla not in tablas:
                continue
            cantidad = connection.execute(
                text(f'SELECT COUNT(*) FROM "{tabla}"')
            ).scalar_one()
            if cantidad == 0:
                connection.execute(text(f'DROP TABLE "{tabla}"'))
                print(f"Tabla legacy eliminada: {tabla}")
            else:
                print(
                    f"Tabla legacy conservada por contener datos: {tabla} "
                    f"({cantidad} registros)"
                )
