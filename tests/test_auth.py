def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "strongpassword123"
    }

    # Register pertama kali (harus sukses)
    response_first = client.post(
        "/auth/register",
        json=payload
    )

    assert response_first.status_code == 201

    # Register kedua kali dengan email yang sama (harus gagal dengan 400)
    response_second = client.post(
        "/auth/register",
        json=payload
    )

    assert response_second.status_code == 400
    assert response_second.json()["detail"] == "Email already exists"


def test_login_success(client):
    payload = {
        "email": "loginuser@example.com", 
        "password": "strongpassword123"
    }

    # Resiter dulu 
    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code == 201

    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"], 
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "unregistered@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data