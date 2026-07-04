import pytest

def test_api_contract_tools_execute(client):
    response = client.post("/api/v1/tools/some_tool/execute", json={"foo": "bar"})
    assert response.status_code == 501
    assert response.json()["detail"] == "feature_available: false"

def test_api_contract_organization_goals(client):
    response = client.post("/api/v1/organization/goals", json={"title": "foo"})
    assert response.status_code == 501
    assert response.json()["detail"] == "feature_available: false"

def test_api_contract_memory_index(client):
    response = client.post("/api/v1/memory", json={"content": "test"})
    assert response.status_code == 501
    assert response.json()["detail"] == "feature_available: false"

def test_api_contract_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code in (200, 500)
