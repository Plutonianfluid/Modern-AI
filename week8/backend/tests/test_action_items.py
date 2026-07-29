def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"

    assert client.get(f"/action-items/{item['id']}").status_code == 200
    assert client.delete(f"/action-items/{item['id']}").status_code == 204
    assert client.get(f"/action-items/{item['id']}").status_code == 404


def test_action_item_validation_and_missing_resources(client):
    assert client.post("/action-items/", json={"description": ""}).status_code == 422
    assert client.put("/action-items/999/complete").status_code == 404
    assert client.patch("/action-items/999", json={"completed": True}).status_code == 404
    assert client.delete("/action-items/999").status_code == 404


def test_action_items_pagination_sorting_and_filtering(client):
    for description in ("Charlie", "Alpha", "Bravo"):
        assert client.post("/action-items/", json={"description": description}).status_code == 201

    alpha = client.get("/action-items/", params={"sort": "description", "limit": 1}).json()
    rest = client.get(
        "/action-items/", params={"sort": "description", "skip": 1, "limit": 2}
    ).json()
    assert [item["description"] for item in alpha] == ["Alpha"]
    assert [item["description"] for item in rest] == ["Bravo", "Charlie"]

    client.patch(f"/action-items/{rest[0]['id']}", json={"completed": True})
    completed = client.get("/action-items/", params={"completed": True}).json()
    assert [item["description"] for item in completed] == ["Bravo"]

    assert client.get("/action-items/", params={"skip": -1}).status_code == 422
    assert client.get("/action-items/", params={"limit": 201}).status_code == 422
    assert client.get("/action-items/", params={"sort": "project"}).status_code == 422
