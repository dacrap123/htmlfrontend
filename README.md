# 10-Second Click Challenge

This project provides a small Flask application that serves an HTML front end for a 10-second clicking game. Players click as many times as possible within the time limit, then submit their score to a shared leaderboard.

## Prerequisites

- Python 3.9+
- A virtual environment (recommended)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install -r requirements.txt
```

## Running the server

```bash
python server.py
```

The application runs on http://127.0.0.1:5000. Open the URL in your browser to play.

## Development notes

- The leaderboard is stored in memory and resets when the server restarts.
- Modify `templates/index.html` to adjust the front-end look or behavior.
