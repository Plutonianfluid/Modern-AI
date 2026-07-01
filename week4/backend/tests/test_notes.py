def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_notes_is_case_insensitive(client):
    # Codex assignment change: this verifies the enhanced search behavior from docs/TASKS.md.
    client.post("/notes/", json={"title": "Sprint Plan", "content": "Discuss API docs"})
    client.post("/notes/", json={"title": "Lunch", "content": "Buy snacks"})

    r = client.get("/notes/search/", params={"q": "sprint"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["title"] == "Sprint Plan"

    r = client.get("/notes/search/", params={"q": "API"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["content"] == "Discuss API docs"
