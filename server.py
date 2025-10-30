from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from threading import Lock
from typing import List

from flask import Flask, jsonify, render_template, request


@dataclass(order=True)
class ScoreEntry:
    score: int
    submitted_at: float
    name: str


class Leaderboard:
    """In-memory leaderboard that keeps the highest scores."""

    def __init__(self, max_entries: int = 10) -> None:
        self._max_entries = max_entries
        self._entries: List[ScoreEntry] = []
        self._lock = Lock()

    def add_score(self, name: str, score: int) -> None:
        """Insert a score entry, keeping the list sorted by score."""
        entry = ScoreEntry(score=score, submitted_at=time.time(), name=name)
        with self._lock:
            self._entries.append(entry)
            # Keep the list sorted descending by score, then ascending by submission time.
            self._entries.sort(key=lambda item: (-item.score, item.submitted_at))
            # Trim the list to the desired length.
            if len(self._entries) > self._max_entries:
                self._entries = self._entries[: self._max_entries]

    def as_dict(self) -> List[dict]:
        with self._lock:
            return [asdict(entry) for entry in self._entries]


app = Flask(__name__)
leaderboard = Leaderboard(max_entries=20)


@app.after_request
def add_cors_headers(response):
    """Allow the front end to talk to the API even when served elsewhere."""
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/api/scores", methods=["GET"])
def get_scores():
    return jsonify({"scores": leaderboard.as_dict()})


@app.route("/api/submit", methods=["POST", "OPTIONS"])
def submit_score():
    if request.method == "OPTIONS":
        # Pre-flight request from browsers using Fetch API.
        response = app.make_default_options_response()
        return response

    data = request.get_json(force=True)
    name = (data.get("name") or "Anonymous").strip()[:30]
    score = int(data.get("score", 0))
    if score < 0:
        return jsonify({"error": "Score must be non-negative."}), 400

    if not name:
        name = "Anonymous"

    leaderboard.add_score(name=name, score=score)
    return jsonify({"ok": True, "scores": leaderboard.as_dict()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
