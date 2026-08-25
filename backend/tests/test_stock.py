from fastapi.testclient import TestClient


def _crear_producto_con_stock(client: TestClient, headers: dict[str, str], stock_inicial: int = 10) -> int:
    evento = client.post(
        "/api/v1/eventos",
        json={"nombre": "Feria", "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-03"},
        headers=headers,
    ).json()
    empresario = client.post(
        "/api/v1/empresarios",
        json={"nombre_negocio": "Negocio X", "propietario": "Prop X"},
        headers=headers,
    ).json()
    stand = client.post(
        "/api/v1/stands",
        json={"id_evento": evento["id_evento"], "id_empresario": empresario["id_empresario"]},
        headers=headers,
    ).json()
    producto = client.post(
        "/api/v1/productos",
        json={"id_stand": stand["id_stand"], "nombre": "Producto X", "stock_inicial": stock_inicial},
        headers=headers,
    ).json()
    return producto["id_producto"]


def test_venta_descuenta_stock(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=10)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 3, "tipo_movimiento": "venta"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["stock_resultante"] == 7


def test_reposicion_incrementa_stock(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=10)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 5, "tipo_movimiento": "reposicion"},
        headers=auth_headers,
    )
    assert r.json()["stock_resultante"] == 15


def test_ajuste_negativo_reduce_stock(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=10)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": -4, "tipo_movimiento": "ajuste"},
        headers=auth_headers,
    )
    assert r.json()["stock_resultante"] == 6


def test_venta_no_puede_dejar_stock_negativo(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=5)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 10, "tipo_movimiento": "venta"},
        headers=auth_headers,
    )
    assert r.status_code == 422

    # el stock no debe haber cambiado
    r = client.get(f"/api/v1/productos/{producto_id}", headers=auth_headers)
    assert r.json()["stock_actual"] == 5


def test_venta_cantidad_no_positiva_rechazada(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=5)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 0, "tipo_movimiento": "venta"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_ajuste_cero_rechazado(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=5)
    r = client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 0, "tipo_movimiento": "ajuste"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_movimiento_producto_inexistente(client: TestClient, auth_headers: dict[str, str]) -> None:
    r = client.post(
        "/api/v1/productos/999999/movimientos",
        json={"cantidad_cambio": 1, "tipo_movimiento": "venta"},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_historial_de_movimientos_ordenado_mas_reciente_primero(client: TestClient, auth_headers: dict[str, str]) -> None:
    producto_id = _crear_producto_con_stock(client, auth_headers, stock_inicial=20)
    client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 1, "tipo_movimiento": "venta"},
        headers=auth_headers,
    )
    client.post(
        f"/api/v1/productos/{producto_id}/movimientos",
        json={"cantidad_cambio": 2, "tipo_movimiento": "reposicion"},
        headers=auth_headers,
    )
    r = client.get(f"/api/v1/productos/{producto_id}/movimientos", headers=auth_headers)
    items = r.json()["items"]
    assert len(items) == 2
    assert items[0]["tipo_movimiento"] == "reposicion"
    assert items[1]["tipo_movimiento"] == "venta"


def test_producto_stand_inexistente_rechazado(client: TestClient, auth_headers: dict[str, str]) -> None:
    r = client.post(
        "/api/v1/productos",
        json={"id_stand": 999999, "nombre": "X", "stock_inicial": 1},
        headers=auth_headers,
    )
    assert r.status_code == 404
