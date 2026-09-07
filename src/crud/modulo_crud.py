from typing import Any
from uuid import UUID

from src.database.connection import get_session
from src.entities.curso import Curso
from src.entities.modulo import Modulo


class ModuloCRUD:
    def crear(self, registro: Modulo) -> Modulo:
        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def crear_para_curso(
        self, curso: Curso, nombre: str, descripcion: str = "", orden: int = 0
    ) -> Modulo:
        return self.crear(
            Modulo(
                nombre=nombre,
                descripcion=descripcion,
                orden=orden,
                id_curso=curso.id_curso,
            )
        )

    def listar(self) -> list[Modulo]:
        session = get_session()
        try:
            return session.query(Modulo).all()
        finally:
            session.close()

    def listar_del_curso(self, curso: Curso) -> list[Modulo]:
        session = get_session()
        try:
            return (
                session.query(Modulo)
                .filter_by(id_curso=curso.id_curso)
                .order_by(Modulo.orden)
                .all()
            )
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Modulo | None:
        session = get_session()
        try:
            return session.query(Modulo).filter_by(id_modulo=identificador).first()
        finally:
            session.close()

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Modulo | None:
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(id_modulo=identificador).first()
            if modulo is None:
                return None
            for nombre, valor in cambios.items():
                if nombre == "nombre":
                    modulo.set_nombre(valor)
                elif nombre == "orden":
                    modulo.set_orden(valor)
                elif nombre in {"descripcion", "id_curso"}:
                    setattr(modulo, nombre, valor)
            session.commit()
            session.refresh(modulo)
            return modulo
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(id_modulo=identificador).first()
            if modulo is None:
                return False
            session.delete(modulo)
            session.commit()
            return True
        finally:
            session.close()
