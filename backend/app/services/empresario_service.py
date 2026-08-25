from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.empresario import Empresario
from app.schemas.common import PaginatedResponse
from app.schemas.empresario import EmpresarioCreate, EmpresarioResponse, EmpresarioUpdate


def get_empresario_or_404(db: Session, empresario_id: int) -> Empresario:
    empresario = db.get(Empresario, empresario_id)
    if empresario is None:
        raise NotFoundError(f"Empresario {empresario_id} no encontrado.")
    return empresario


def list_empresarios(
    db: Session, page: int, page_size: int, tipo_producto: str | None = None
) -> PaginatedResponse[EmpresarioResponse]:
    stmt = select(Empresario)
    if tipo_producto:
        stmt = stmt.where(Empresario.tipo_producto == tipo_producto)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(Empresario.id_empresario).offset((page - 1) * page_size).limit(page_size)
    ).all()

    return PaginatedResponse[EmpresarioResponse](
        items=[EmpresarioResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def create_empresario(db: Session, data: EmpresarioCreate) -> Empresario:
    empresario = Empresario(**data.model_dump())
    db.add(empresario)
    db.commit()
    db.refresh(empresario)
    return empresario


def update_empresario(db: Session, empresario: Empresario, data: EmpresarioUpdate) -> Empresario:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(empresario, field, value)
    db.commit()
    db.refresh(empresario)
    return empresario


def delete_empresario(db: Session, empresario: Empresario) -> None:
    db.delete(empresario)
    db.commit()
