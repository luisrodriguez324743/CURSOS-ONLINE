from src.entities.rol import Rol
from .base_crud import CRUD


class RolCRUD(CRUD[Rol]):
    def __init__(self) -> None:
        super().__init__(Rol)

    def buscar_por_nombre(self, nombre: str) -> Rol | None:
        """Permite encontrar un rol rápidamente por su nombre exacto o sin importar mayúsculas."""
        nombre_clean = nombre.strip().lower()
        return next(
            (
                rol
                for rol in self.registros.values()
                if rol.nombre.strip().lower() == nombre_clean
            ),
            None,
        )
