from httpx import AsyncClient
from tests.conftest import ac, session
import pytest


@pytest.mark.parametrize("name,password,status_code", [
    ("Alexander", "123456789", 200),
    ("Alexander", "987654321", 409),
    ("123", "1234", 200),
    ("1234", "123", 200)
])
async def test_register_user(name, password, status_code, ac: AsyncClient):
    response = await ac.post("/user/register", json={
        "name": name,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("name,password,status_code", [
    ("Alexander", "123456789", 200),
    ("Alexander", "987654321", 401),
    ("Ivan", "123456789", 401)
])
async def test_login_user(name, password, status_code, ac: AsyncClient):
    response = await ac.post("/user/login", json={
        "name": name,
        "password": password
    })

    assert response.status_code == status_code