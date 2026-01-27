import pytest

@pytest.fixture()
def subject(client):
    subject = client.post("/subjects/create/", json={"name": "2-yunalish"})
    return subject.json()


def test_create_subject(client):
    response = client.post("/subjects/create/", json={"name": "1-yunalish"})
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "1-yunalish"
    assert "id" in data


def test_get_subject(client, subject):
    sub_id  = subject['id']

    response = client.get(f"/subjects/{sub_id}/")

    assert response.status_code == 200
    assert response.json()["name"] == subject["name"]
    assert response.json()["id"] == sub_id


def test_update_subject(client, subject):
    sub_id = subject['id']

    response = client.patch(f"/subjects/update/{sub_id}/", json={"name": "10-yunalish"})
    assert response.status_code == 200
    assert response.json()["name"] == "10-yunalish"
    assert response.json()["id"] == sub_id
    

def test_delete_subject(client, subject):
    sub_id = subject["id"]

    response = client.delete(f"/subjects/delete/{sub_id}/")
    assert response.status_code == 200
    assert response.json()["status_code"] == 204


def test_subject_not_found(client):
    response = client.get("/subjects/222/")
    assert response.status_code == 404