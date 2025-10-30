import pathlib
import sys

import pytest

pytest.importorskip("flask")

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server import app, leaderboard


@pytest.fixture(autouse=True)
def clear_leaderboard():
    leaderboard.clear()
    yield
    leaderboard.clear()


def test_index_page_renders():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"10-Second Click Challenge" in response.data


def test_submit_and_fetch_scores():
    client = app.test_client()
    submit_response = client.post("/api/submit", json={"name": "Tester", "score": 7})
    assert submit_response.status_code == 200
    data = submit_response.get_json()
    assert data["ok"] is True
    assert data["scores"][0]["name"] == "Tester"
    assert data["scores"][0]["score"] == 7

    scores_response = client.get("/api/scores")
    assert scores_response.status_code == 200
    scores = scores_response.get_json()["scores"]
    assert len(scores) == 1
    assert scores[0]["name"] == "Tester"
    assert scores[0]["score"] == 7


def test_submit_rejects_negative_scores():
    client = app.test_client()
    response = client.post("/api/submit", json={"name": "Bad", "score": -1})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
