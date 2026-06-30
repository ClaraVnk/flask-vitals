# flask-vitals

**A drop-in Flask health blueprint: `/healthz` (liveness) and `/readyz` (readiness).**

Two lines in any Flask app give you the liveness/readiness split that external
monitors ([Huginn](https://github.com/ClaraVnk/huginn), UptimeRobot, Uptime
Kuma) and orchestrators (Kubernetes) expect — so monitoring an app is just
"point a monitor at `/healthz`", no bespoke endpoint per app.

## What

| Endpoint    | Meaning                                   | Status |
| ----------- | ----------------------------------------- | ------ |
| `/healthz`  | The process is up (no dependencies probed) | always `200` |
| `/readyz`   | Every registered check passes (DB, cache…) | `200` if all pass, else `503` |

`/readyz` returns a per-check breakdown, e.g. `{"ready": false, "checks": {"db": false}}`,
so a "up but broken" app (process alive, database down) is caught.

## Run

```python
from flask import Flask
from sqlalchemy import text
from flask_vitals import vitals

app = Flask(__name__)

def db_ok() -> None:
    db.session.execute(text("SELECT 1"))   # raises → not ready

app.register_blueprint(vitals(checks={"db": db_ok}, version="1.4.2"))
```

- `checks`: a `{name: callable}` map. A check **passes** unless it returns
  `False` or raises (a `None`/truthy return passes).
- `version`: optional, echoed by `/healthz`.
- `liveness_path` / `readiness_path`: defaults `/healthz` and `/readyz`.

Install (until published): `uv add path/to/flask-vitals` or
`pip install path/to/flask-vitals`.

### Monitoring it from Huginn

In Huginn's **Uptime** panel, add per app:
- an **HTTP** monitor on `…/healthz` (expected status `200`) — is it alive?
- a **keyword** monitor on `…/readyz` containing `"ready": true` — is it serving?

## Test

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

## Deploy

A library — published to an index (`uv build` → `uv publish`) or vendored. No
service to run.

## Architecture

One module, `flask_vitals.blueprint`, exposing `vitals(...) -> flask.Blueprint`.
No state, no dependencies beyond Flask; readiness checks are injected by the host
app, so the library never reaches into your stack.
