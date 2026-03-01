"""Tests for main routes."""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Index page returns 200."""
    rv = client.get("/")
    assert rv.status_code == 200


def test_health(client):
    """Health check returns 200 and status ok."""
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("status") == "ok"
