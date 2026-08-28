from src.entities.usuario import Usuario
from .base_crud import CRUD


class UsuarioCRUD(CRUD[Usuario]):
    def __init__(self) -> None:
        super().__init__(Usuario)

    def buscar_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        return next(
            (
                usuario
                for usuario in self.registros.values()
                if usuario.nombre_usuario == nombre_usuario
            ),
            None,
        )

    def autenticar(self, nombre_usuario: str, password: str) -> Usuario | None:
        return next(
            (
                usuario
                for usuario in self.registros.values()
                if usuario.nombre_usuario == nombre_usuario
                and usuario.password == password
            ),
            None,
        )
