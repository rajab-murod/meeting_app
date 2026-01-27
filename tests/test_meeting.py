import pytest
import datetime

@pytest.fixture
def edu_year(client):
    year = client.post("/edu_year/create/", json={"name":"2025-2026"})
    return year.json()


@pytest.fixture
def meeting(client, edu_year):
    response = client.post("/meetings/create/", json={
        "name": "1-yigilish",
        "life_time": str(datetime.datetime.now()),
        "input_time": str(datetime.datetime.now()),
        "edu_year_id": edu_year['id']
        })
    return response.json()


def test_create_meeting(client, edu_year):
    response = client.post("/meetings/create/", json={
        "name": "2-yigilish",
        "life_time": str(datetime.datetime.now()),
        "input_time": str(datetime.datetime.now()),
        "edu_year_id": edu_year['id']
        })
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["edu_year"]["id"] == edu_year["id"]


def test_get_meeting(client, meeting, edu_year):
    m_id = meeting['id']

    response = client.get(f"/meetings/{m_id}/")

    assert response.status_code == 200
    assert response.json()["name"] == meeting["name"]
    assert response.json()["id"] == meeting["id"]
    assert response.json()["edu_year"]["id"] == edu_year["id"]


def test_update_meeting(client, meeting):
    m_id = meeting["id"]
    response = client.patch(f"/meetings/update/{m_id}/", json={
        "name": "123-yigilish",
        "life_time": "2026-02-27T16:41:45",
        "input_time": "2026-02-26T16:41:45",
        "is_confirm": True

    })

    assert response.status_code == 200
    assert response.json()["name"] == "123-yigilish"
    assert response.json()["id"] == m_id
    assert response.json()["is_confirm"] == True


def test_delete_meeting(client, meeting):
    m_id = meeting["id"]

    response = client.delete(f"/meetings/delete/{m_id}/")
    assert response.status_code == 200
    assert response.json()["status_code"] == 204


def test_stat_meeting(client):
    response = client.get("/meetings/stat_by_month/")

    assert response.status_code == 200
    assert "month" in response.json()[0]
    assert "count" in response.json()[0]
