from fastapi.testclient import TestClient

def create_user_and_get_token(
        client: TestClient,
        email: str = "user@example.com",
        password: str = "strongpassword123",
) -> str: 
    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Login user 
    login_response = client.post(
        "/auth/login",
        data={
            "username": email, 
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return token

def test_create_task(client):
    token =create_user_and_get_token(client)

    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Testing task creation",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Testing task creation"
    assert data["is_completed"] is False
    assert "id" in data

def test_list_tasks(client):
    token = create_user_and_get_token(client)

    client.post(
        "/tasks/",
        json={"title": "Task 1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        "/tasks/",
        json={"title": "Task 2"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {task["title"] for task in data} == {"Task 1", "Task 2"}

def test_get_task(client):
    token = create_user_and_get_token(client)

    create_response = client.post(
        "/tasks/",
        json={"title": "Single Task"},
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Single Task"

def test_update_task(client): 
    token = create_user_and_get_token(client)

    create_response = client.post(
        "/tasks/",
        json={"title": "Original Title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"is_completed": True},   # partial update, cuma satu field
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] is True
    assert data["title"] == "Original Title" # field yang tidak dikirmkan harus tetap utuh

def test_delete_task(client): 
    token = create_user_and_get_token(client)

    create_response = client.post(
        "/tasks/",
        json={"title": "To Be Deleted"}, 
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204

    # Verifikasi task benar-benar hilang, bukan cuma percaya status code delete
    get_response = client.get(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404

def test_user_cannot_access_other_users_task(client): 
    token_a = create_user_and_get_token(client, email="usera@example.com")
    token_b = create_user_and_get_token(client, email="userb@example.com")

    create_response = client.post(
        "/tasks/",
        json={"title": "User A's private task"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    task_id = create_response.json()["id"]

    # User B coba GET task milik User A
    get_response = client.get(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token_b}"}
    )
    assert get_response.status_code == 404 # bukan 403, sesuai reasoning IDOR

    # User B coba UPDATE task milik User A
    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Hijacked"},
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert update_response.status_code == 404

    # User B coba Delete task milik User A
    delete_response = client.delete(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token_b}"}
    )
    assert delete_response.status_code == 404

    # Pembuktian akhir: task itu masih ada dan utuh untuk User A
    verify_response = client.get(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token_a}"}
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["title"] == "User A's private task"