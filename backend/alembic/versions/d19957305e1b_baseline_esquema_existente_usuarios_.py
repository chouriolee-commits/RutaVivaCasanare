"""baseline: esquema existente (usuarios, empresarios, eventos, stands, productos, movimientos_stock)

Esta revisión es intencionalmente un no-op. Las tablas ya existían en la
base de datos (creadas manualmente vía phpMyAdmin) antes de introducir
Alembic en el proyecto. En vez de aplicar los ALTER cosméticos que
`--autogenerate` detectó (nullability de columnas con server_default,
y el nombre del índice único de `usuarios.email`), se fija esta revisión
como punto de partida con `alembic stamp head` — sin tocar la BD real —
para que las migraciones futuras (`alembic revision --autogenerate`) se
calculen a partir de aquí.

Revision ID: d19957305e1b
Revises:
Create Date: 2026-08-24 22:22:54.471920

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'd19957305e1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op: el esquema ya existe en la base de datos."""
    pass


def downgrade() -> None:
    """No-op: ver docstring del módulo."""
    pass
