from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioUpdate


def update_usuario(db: Session, usuario: Usuario, data: UsuarioUpdate) -> Usuario:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario
