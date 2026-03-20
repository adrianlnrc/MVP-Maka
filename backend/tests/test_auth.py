def test_register(client):
    response = client.post("/api/auth/register", json={
        "full_name": "Maria Silva",
        "email": "maria@teste.com",
        "password": "senha123",
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login(client):
    # Register first
    client.post("/api/auth/register", json={
        "full_name": "João Teste",
        "email": "joao@teste.com",
        "password": "senha456",
    })
    # Then login
    response = client.post("/api/auth/login", json={
        "email": "joao@teste.com",
        "password": "senha456",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "full_name": "Ana Teste",
        "email": "ana@teste.com",
        "password": "senha789",
    })
    response = client.post("/api/auth/login", json={
        "email": "ana@teste.com",
        "password": "senhaerrada",
    })
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_with_token(client):
    reg = client.post("/api/auth/register", json={
        "full_name": "Pedro Auth",
        "email": "pedro@teste.com",
        "password": "pedro1234",
    })
    token = reg.json()["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "pedro@teste.com"


def test_duplicate_email(client):
    data = {"full_name": "Lucas Dup", "email": "lucas@dup.com", "password": "senha123"}
    client.post("/api/auth/register", json=data)
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 409
