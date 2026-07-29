def test_create_project_and_assign_action_items(client):
    response = client.post("/projects/", json={"name": "Launch", "description": "Website launch"})
    assert response.status_code == 201
    project = response.json()

    response = client.post(
        "/action-items/",
        json={"description": "Prepare release notes", "project_id": project["id"]},
    )
    assert response.status_code == 201
    item = response.json()
    assert item["project_id"] == project["id"]

    filtered = client.get("/action-items/", params={"project_id": project["id"]})
    assert [row["id"] for row in filtered.json()] == [item["id"]]

    response = client.patch(f"/action-items/{item['id']}", json={"project_id": None})
    assert response.status_code == 200
    assert response.json()["project_id"] is None


def test_project_listing_duplicates_and_missing_project(client):
    for name in ("Zulu", "Alpha"):
        assert client.post("/projects/", json={"name": name}).status_code == 201

    projects = client.get("/projects/", params={"limit": 1}).json()
    assert [project["name"] for project in projects] == ["Alpha"]
    assert client.get(f"/projects/{projects[0]['id']}").status_code == 200

    assert client.post("/projects/", json={"name": "Alpha"}).status_code == 409
    assert client.get("/projects/999").status_code == 404
    assert client.post("/projects/", json={"name": ""}).status_code == 422
