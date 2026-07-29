def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_note_validation_and_missing_resources(client):
    assert client.post("/notes/", json={"title": "", "content": "body"}).status_code == 422
    assert client.post("/notes/", json={"title": "title", "content": ""}).status_code == 422
    assert client.patch("/notes/999", json={"title": "missing"}).status_code == 404
    assert client.delete("/notes/999").status_code == 404


def test_notes_pagination_sorting_and_invalid_parameters(client):
    for title in ("Charlie", "Alpha", "Bravo"):
        response = client.post("/notes/", json={"title": title, "content": f"{title} body"})
        assert response.status_code == 201

    first_page = client.get("/notes/", params={"sort": "title", "skip": 0, "limit": 2})
    second_page = client.get("/notes/", params={"sort": "title", "skip": 2, "limit": 2})
    assert [note["title"] for note in first_page.json()] == ["Alpha", "Bravo"]
    assert [note["title"] for note in second_page.json()] == ["Charlie"]

    descending = client.get("/notes/", params={"sort": "-title"})
    assert [note["title"] for note in descending.json()] == ["Charlie", "Bravo", "Alpha"]

    assert client.get("/notes/", params={"skip": -1}).status_code == 422
    assert client.get("/notes/", params={"limit": 0}).status_code == 422
    assert client.get("/notes/", params={"sort": "not_a_column"}).status_code == 422
