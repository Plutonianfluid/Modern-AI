def create_item(client, description):
    response = client.post("/action-items/", json={"description": description})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_complete_filter_and_paginate(client):
    first = create_item(client, "Ship it")
    create_item(client, "Write docs")
    assert client.put(f"/action-items/{first['id']}/complete").status_code == 200

    completed = client.get("/action-items/", params={"completed": True}).json()
    assert completed["total"] == 1
    assert completed["items"][0]["completed"] is True
    open_items = client.get("/action-items/", params={"completed": False}).json()
    assert open_items["total"] == 1
    assert open_items["items"][0]["description"] == "Write docs"

    assert client.get("/action-items/", params={"page": 2, "page_size": 2}).json()["items"] == []
    assert client.get("/action-items/", params={"page_size": 101}).status_code == 422


def test_bulk_complete_is_all_or_nothing(client):
    first = create_item(client, "One")
    second = create_item(client, "Two")
    response = client.post("/action-items/bulk-complete", json={"ids": [first["id"], 9999]})
    assert response.status_code == 404
    open_items = client.get("/action-items/", params={"completed": False}).json()
    assert open_items["total"] == 2

    response = client.post("/action-items/bulk-complete", json={"ids": [first["id"], second["id"]]})
    assert response.status_code == 200
    assert all(item["completed"] for item in response.json())
    assert client.get("/action-items/", params={"completed": False}).json()["total"] == 0


def test_action_item_errors_and_validation(client):
    assert client.post("/action-items/", json={"description": "   "}).status_code == 422
    assert client.post("/action-items/bulk-complete", json={"ids": []}).status_code == 422
    assert client.post("/action-items/bulk-complete", json={"ids": [1, 1]}).status_code == 400
    assert client.put("/action-items/999/complete").status_code == 404
