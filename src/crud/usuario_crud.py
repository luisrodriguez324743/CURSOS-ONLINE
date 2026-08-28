from src.entities.usuario import Usuario
from .base_crud import CRUD


class UsuarioCRUD(CRUD[Usuario]):
    def __init__(self) -> None:
        super().__init__(Usuario)

    def buscar_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        nombre_clean = nombre_usuario.strip().lower()
        return next(
            (
                usuario
                for usuario in self.registros.values()
                if usuario.nombre_usuario.strip().lower() == nombre_clean
            ),
            None,
        )

    def autenticar(self, nombre_usuario: str, password: str) -> Usuario | None:
        nombre_clean = nombre_usuario.strip().lower()
        return next(
            (
                usuario
                for usuario in self.registros.values()
                if usuario.nombre_usuario.strip().lower() == nombre_clean
                and usuario.password == password
            ),
            None,
        )
