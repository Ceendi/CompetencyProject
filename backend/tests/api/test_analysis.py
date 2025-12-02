from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.models import Film, Job, Analysis


def test_initiate_analysis(client: TestClient, db: Session):
    url = "https://www.youtube.com/watch?v=test1"

    with patch("app.orchestrator.pipeline.run_full_pipeline") as mock_pipeline:
        response = client.post("/api/analysis/", json={"url": url})

        assert response.status_code == 202
        data = response.json()
        assert data["url"] == url
        assert data["status"] == "pending"
        assert "id" in data

        job = db.query(Job).filter(Job.url == url).first()
        assert job is not None
        assert job.status == "pending"

        mock_pipeline.assert_called_once()


def test_initiate_analysis_duplicate(client: TestClient, db: Session):
    url = "https://www.youtube.com/watch?v=test2"

    film = Film(url=url, id=1)
    db.add(film)
    db.commit()

    response = client.post("/api/analysis/", json={"url": url})

    assert response.status_code in [200, 202]
    data = response.json()

    assert data["status"] == "complete"
    assert data["film_id"] == 1
    assert data["url"] == url
    assert data["id"] > 0


def test_initiate_analysis_conflict(client: TestClient, db: Session):
    url = "https://www.youtube.com/watch?v=test3"

    job = Job(url=url, status="analyzing")
    db.add(job)
    db.commit()

    response = client.post("/api/analysis/", json={"url": url})

    assert response.status_code in [200, 202]
    data = response.json()
    assert data["id"] == job.id
    assert "in progress" not in str(data)


def test_get_status(client: TestClient, db: Session):
    job = Job(url="http://test.com/status", status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)

    response = client.get(f"/api/status/{job.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["id"] == job.id


def test_get_status_not_found(client: TestClient):
    response = client.get("/api/status/9999")
    assert response.status_code == 404


def test_get_result(client: TestClient, db: Session):
    film = Film(url="http://test.com/result", id=10)
    db.add(film)
    db.commit()

    analysis = Analysis(
        film_id=10,
        battery=0.85,
        screen=0.9,
        price=0.5
    )
    db.add(analysis)
    db.commit()

    response = client.get(f"/api/result/{film.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "http://test.com/result"
    assert data["id"] == 10
    assert data["analysis"]["battery"] == 0.85


def test_get_result_not_found(client: TestClient):
    response = client.get("/api/result/9999")
    assert response.status_code == 404
