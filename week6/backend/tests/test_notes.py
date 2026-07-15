def create_note(client, title="Test", content="Hello world"):
    response = client.post("/notes/", json={"title": title, "content": content})
    assert response.status_code == 201, response.text
    return response.json()


def test_notes_crud(client):
    note = create_note(client)
    assert client.get(f"/notes/{note['id']}").json()["title"] == "Test"

    response = client.put(
        f"/notes/{note['id']}", json={"title": "Updated", "content": "New content"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404
    assert (
        client.put(f"/notes/{note['id']}", json={"title": "X", "content": "Y"}).status_code == 404
    )
    assert client.delete(f"/notes/{note['id']}").status_code == 404


def test_note_validation(client):
    for payload in (
        {"title": "", "content": "content"},
        {"title": "   ", "content": "content"},
        {"title": "title", "content": ""},
        {"title": "x" * 201, "content": "content"},
    ):
        assert client.post("/notes/", json=payload).status_code == 422


def test_search_is_case_insensitive_sorted_and_paginated(client):
    create_note(client, "zebra", "Needle one")
    create_note(client, "Alpha", "needle two")
    create_note(client, "middle NEEDLE", "other")
    create_note(client, "Unrelated", "nothing")

    response = client.get(
        "/notes/search", params={"q": "NeEdLe", "sort": "title_asc", "page_size": 2}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["total"] == 3
    assert [item["title"] for item in data["items"]] == ["Alpha", "middle NEEDLE"]

    second = client.get(
        "/notes/search", params={"q": "needle", "sort": "title_asc", "page": 2, "page_size": 2}
    ).json()
    assert [item["title"] for item in second["items"]] == ["zebra"]


def test_list_pagination_boundaries(client):
    for index in range(3):
        create_note(client, f"Note {index}", "content")
    data = client.get("/notes/", params={"page": 2, "page_size": 2}).json()
    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert client.get("/notes/", params={"page": 3, "page_size": 2}).json()["items"] == []
    assert client.get("/notes/", params={"page": 0}).status_code == 422
    assert client.get("/notes/", params={"page_size": 101}).status_code == 422
    assert client.get("/notes/search", params={"sort": "invalid"}).status_code == 422
