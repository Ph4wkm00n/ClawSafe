import pytest


@pytest.mark.anyio
async def test_list_templates(client):
    resp = await client.get("/api/v1/templates")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Default seeded templates
    names = [t["name"] for t in data]
    assert "default_slack" in names
    assert "default_teams" in names
    assert "default_email" in names


@pytest.mark.anyio
async def test_get_template(client):
    resp = await client.get("/api/v1/templates/default_slack")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "default_slack"
    assert data["channel"] == "slack"


@pytest.mark.anyio
async def test_get_nonexistent_template(client):
    resp = await client.get("/api/v1/templates/nonexistent")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_create_template(client):
    resp = await client.post("/api/v1/templates", json={
        "name": "my_custom",
        "channel": "slack",
        "template_text": "Hello {{ name }}!",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "my_custom"
