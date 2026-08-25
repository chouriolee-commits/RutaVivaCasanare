from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError, ValidationDomainError
from app.models.movimiento_stock import MovimientoStock, TipoMovimientoEnum
from app.models.producto import Producto
from app.schemas.common import PaginatedResponse
from app.schemas.movimiento_stock import MovimientoStockCreate, MovimientoStockResponse


def _calcular_nuevo_stock(stock_actual: int, data: MovimientoStockCreate) -> int:
    if data.tipo_movimiento == TipoMovimientoEnum.venta:
        return stock_actual - data.cantidad_cambio
    if data.tipo_movimiento == TipoMovimientoEnum.reposicion:
        return stock_actual + data.cantidad_cambio
    # ajuste: cantidad_cambio ya viene con signo (positivo o negativo)
    return stock_actual + data.cantidad_cambio


def registrar_movimiento(db: Session, producto_id: int, data: MovimientoStockCreate) -> MovimientoStock:
    """
    Aplica un movimiento de inventario de forma atómica:
      1. Bloquea la fila del producto (SELECT ... FOR UPDATE) para evitar
         condiciones de carrera si dos ventas llegan al mismo tiempo.
      2. Calcula el nuevo stock y valida que no quede negativo.
      3. Actualiza productos.stock_actual e inserta el registro histórico
         en la misma transacción (todo o nada).
    """
    producto = db.scalar(select(Producto).where(Producto.id_producto == producto_id).with_for_update())
    if producto is None:
        raise NotFoundError(f"Producto {producto_id} no encontrado.")

    nuevo_stock = _calcular_nuevo_stock(producto.stock_actual, data)
    if nuevo_stock < 0:
        raise ValidationDomainError(
            f"Stock insuficiente: quedarían {nuevo_stock} unidades "
            f"(stock actual: {producto.stock_actual}, cambio solicitado: {data.cantidad_cambio})."
        )

    movimiento = MovimientoStock(
        id_producto=producto_id,
        cantidad_cambio=data.cantidad_cambio,
        tipo_movimiento=data.tipo_movimiento,
    )
    producto.stock_actual = nuevo_stock
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    db.refresh(producto)

    # Atributo transitorio (no es columna) para exponer en la respuesta
    # el stock resultante sin que el cliente tenga que hacer otra consulta.
    movimiento.stock_resultante = producto.stock_actual
    return movimiento


def list_movimientos(
    db: Session, page: int, page_size: int, producto_id: int | None = None
) -> PaginatedResponse[MovimientoStockResponse]:
    """Historial de movimientos, más recientes primero. `stock_resultante`
    queda en null aquí (ver docstring del schema); solo se conoce con
    certeza en el momento de registrar el movimiento."""
    stmt = select(MovimientoStock)
    if producto_id is not None:
        stmt = stmt.where(MovimientoStock.id_producto == producto_id)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    # fecha_hora tiene resolución de segundo: id_movimiento desempata movimientos
    # simultáneos manteniendo el orden real de inserción.
    rows = db.scalars(
        stmt.order_by(MovimientoStock.fecha_hora.desc(), MovimientoStock.id_movimiento.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    items = [MovimientoStockResponse.model_validate(row) for row in rows]
    return PaginatedResponse[MovimientoStockResponse](items=items, total=total, page=page, page_size=page_size)
