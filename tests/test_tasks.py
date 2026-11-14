import pytest


def create_task(client, headers, **overrides):
    payload = {"title": "Database quiz prep", "description": "ER diagrams", "priority": "High", "due_date": "2030-01-15"}
    payload.update(overrides)
    return client.post("/tasks", json=payload, headers=headers)


def test_create_and_list_tasks(client, auth):
    res = create_task(client, auth)
    assert res.status_code == 200
    task = res.json()
    assert task["title"] == "Database quiz prep"
    assert task["priority"] == "High"
    assert task["due_date"] == "2030-01-15"
    assert task["completed"] is False

    tasks = client.get("/tasks", headers=auth).json()
    assert [t["id"] for t in tasks] == [task["id"]]


def test_tasks_are_listed_newest_first(client, auth):
    first = create_task(client, auth, title="First").json()
    second = create_task(client, auth, title="Second").json()
    ids = [t["id"] for t in client.get("/tasks", headers=auth).json()]
    assert ids == [second["id"], first["id"]]


def test_description_and_due_date_are_optional(client, auth):
    res = client.post("/tasks", json={"title": "Buy notebook"}, headers=auth)
    assert res.status_code == 200
    assert res.json()["priority"] == "Medium"
    assert res.json()["due_date"] is None


@pytest.mark.parametrize(
    "overrides",
    [{"title": ""}, {"title": "   "}, {"priority": "Urgent"}, {"due_date": "not-a-date"}],
    ids=["empty-title", "blank-title", "unknown-priority", "bad-date"],
)
def test_create_rejects_invalid_input(client, auth, overrides):
    assert create_task(client, auth, **overrides).status_code == 422


def test_update_changes_only_the_fields_sent(client, auth):
    task = create_task(client, auth).json()
    res = client.put(f"/tasks/{task['id']}", json={"title": "Updated title"}, headers=auth)
    assert res.status_code == 200
    updated = res.json()
    assert updated["title"] == "Updated title"
    assert updated["priority"] == "High"
    assert updated["due_date"] == "2030-01-15"


def test_update_can_clear_the_due_date(client, auth):
    task = create_task(client, auth).json()
    res = client.put(f"/tasks/{task['id']}", json={"due_date": None}, headers=auth)
    assert res.status_code == 200
    assert res.json()["due_date"] is None


def test_toggle_marks_done_and_undone(client, auth):
    task = create_task(client, auth).json()
    assert client.patch(f"/tasks/{task['id']}/toggle", headers=auth).json()["completed"] is True
    assert client.patch(f"/tasks/{task['id']}/toggle", headers=auth).json()["completed"] is False


def test_delete_task(client, auth):
    task = create_task(client, auth).json()
    assert client.delete(f"/tasks/{task['id']}", headers=auth).status_code == 200
    assert client.get("/tasks", headers=auth).json() == []


def test_missing_task_returns_404(client, auth):
    assert client.put("/tasks/999", json={"title": "x"}, headers=auth).status_code == 404
    assert client.patch("/tasks/999/toggle", headers=auth).status_code == 404
    assert client.delete("/tasks/999", headers=auth).status_code == 404


def test_tasks_require_login(client):
    assert client.get("/tasks").status_code in (401, 403)
    assert client.post("/tasks", json={"title": "x"}).status_code in (401, 403)


# ---------------- Users must never see each other's data ----------------


def test_users_only_see_their_own_tasks(client, make_user):
    alice = make_user(email="alice@example.com")
    bob = make_user(email="bob@example.com")
    create_task(client, alice, title="Alice's task")

    assert client.get("/tasks", headers=bob).json() == []
    assert [t["title"] for t in client.get("/tasks", headers=alice).json()] == ["Alice's task"]


def test_users_cannot_change_or_delete_other_users_tasks(client, make_user):
    alice = make_user(email="alice@example.com")
    bob = make_user(email="bob@example.com")
    task_id = create_task(client, alice).json()["id"]

    assert client.put(f"/tasks/{task_id}", json={"title": "Hacked"}, headers=bob).status_code == 404
    assert client.patch(f"/tasks/{task_id}/toggle", headers=bob).status_code == 404
    assert client.delete(f"/tasks/{task_id}", headers=bob).status_code == 404

    # Alice's task is untouched
    task = client.get("/tasks", headers=alice).json()[0]
    assert task["title"] == "Database quiz prep"
    assert task["completed"] is False
