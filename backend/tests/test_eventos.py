from fastapi.testclient import TestClient


def _crear_evento(client: TestClient, headers: dict[str, str], **overrides) -> dict:
    payload = {
        "nombre": "Feria Cultural",
        "fecha_inicio": "2026-09-01",
        "fecha_fin": "2026-09-03",
        "ubicacion": "Yopal",
        **overrides,
    }
    r = client.post("/api/v1/eventos", json=payload, headers=headers)
    assert r.status_code == 201, r.text
    return r.json()


def test_list_events_public(client: TestClient) -> None:
    r = client.get("/api/v1/eventos")
    assert r.status_code == 200
    assert r.json()["items"] == []


def test_create_event_no_token(client: TestClient) -> None:
    r = client.post("/api/v1/eventos", json={"nombre": "X", "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-02"})
    assert r.status_code == 401


def test_create_event_with_token(client: TestClient, auth_headers: dict[str, str]) -> None:
    evento = _crear_evento(client, auth_headers)
    assert evento["estado"] == "planeado"


def test_fecha_fin_antes_de_fecha_inicio_rechazada(client: TestClient, auth_headers: dict[str, str]) -> None:
    r = client.post(
        "/api/v1/eventos",
        json={"nombre": "X", "fecha_inicio": "2026-09-05", "fecha_fin": "2026-09-01"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_filter_by_estado(client: TestClient, auth_headers: dict[str, str]) -> None:
    _crear_evento(client, auth_headers, nombre="Evento Planeado", estado="planeado")
    _crear_evento(client, auth_headers, nombre="Evento Finalizado", estado="finalizado")

    r = client.get("/api/v1/eventos", params={"estado": "finalizado"})
    assert r.status_code == 200
    items = r.json()["items"]
    assert len(items) == 1
    assert items[0]["nombre"] == "Evento Finalizado"


def test_update_event(client: TestClient, auth_headers: dict[str, str]) -> None:
    evento = _crear_evento(client, auth_headers)
    r = client.put(
        f"/api/v1/eventos/{evento['id_evento']}",
        json={"nombre": "Feria Actualizada"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["nombre"] == "Feria Actualizada"


def test_update_event_no_token(client: TestClient, auth_headers: dict[str, str]) -> None:
    evento = _crear_evento(client, auth_headers)
    r = client.put(f"/api/v1/eventos/{evento['id_evento']}", json={"nombre": "X"})
    assert r.status_code == 401


def test_delete_event(client: TestClient, auth_headers: dict[str, str]) -> None:
    evento = _crear_evento(client, auth_headers)
    r = client.delete(f"/api/v1/eventos/{evento['id_evento']}", headers=auth_headers)
    assert r.status_code == 204
    r = client.get(f"/api/v1/eventos/{evento['id_evento']}")
    assert r.status_code == 404


def test_get_evento_inexistente(client: TestClient) -> None:
    r = client.get("/api/v1/eventos/999999")
    assert r.status_code == 404


def test_pagination(client: TestClient, auth_headers: dict[str, str]) -> None:
    for i in range(5):
        _crear_evento(client, auth_headers, nombre=f"Evento {i}")

    r = client.get("/api/v1/eventos", params={"page": 1, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] == 5
    assert body["page"] == 1
    assert body["page_size"] == 2
