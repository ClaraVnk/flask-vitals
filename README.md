<div align="center">

# 🩺 flask-vitals

**A drop-in Flask health blueprint — `/healthz` (liveness) + `/readyz` (readiness) in two lines.**

[![PyPI](https://img.shields.io/pypi/v/flask-vitals.svg?logo=pypi&logoColor=white)](https://pypi.org/project/flask-vitals/)
[![CI](https://github.com/ClaraVnk/flask-vitals/actions/workflows/ci.yml/badge.svg)](https://github.com/ClaraVnk/flask-vitals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-2A6DB2.svg)](https://mypy-lang.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

</div>

---

Every service needs the same two endpoints — *"are you alive?"* and *"can you serve?"* —
yet everyone re-writes them, slightly differently, in every app. **flask-vitals** is
the boring, correct version you register once:

```python
from flask_vitals import vitals

app.register_blueprint(vitals())
```

…and now `GET /healthz` and `GET /readyz` answer exactly the way orchestrators
(Kubernetes), load balancers, and external monitors
([Huginn](https://github.com/ClaraVnk/huginn), UptimeRobot, Uptime Kuma) expect.

## ✨ Features

- **Liveness vs. readiness, done right** — `/healthz` says the process is up;
  `/readyz` says it can actually serve (its dependencies are reachable).
- **Injected checks** — readiness probes your DB / cache / queue via callables
  *you* provide; the library never reaches into your stack.
- **Honest status codes** — `/readyz` returns **`503`** with a per-check
  breakdown when something is down, so "up but broken" is caught.
- **Zero config to start, fully tunable** — custom paths, an optional version
  string, any number of named checks.
- **Tiny & typed** — one module, no dependency beyond Flask, `mypy --strict`,
  100 % tested. MIT-licensed.

## 📦 Install

```bash
pip install flask-vitals
# or
uv add flask-vitals
```

## 🚀 Quickstart

```python
from flask import Flask
from sqlalchemy import text
from flask_vitals import vitals

app = Flask(__name__)

def db_ok() -> None:
    db.session.execute(text("SELECT 1"))   # raises → not ready

app.register_blueprint(vitals(checks={"db": db_ok}, version="1.4.2"))
```

| Request        | Response                                                        | Code |
| -------------- | -------------------------------------------------------------- | ---- |
| `GET /healthz` | `{"status": "ok", "version": "1.4.2"}`                         | `200` |
| `GET /readyz`  | `{"ready": true, "checks": {"db": true}}`                      | `200` |
| `GET /readyz`  | `{"ready": false, "checks": {"db": false}}` *(db unreachable)* | `503` |

A check **passes** unless it returns `False` or raises — so a one-liner like
`lambda: cache.ping()` is a valid check.

### Options

| Argument         | Default      | Purpose                                   |
| ---------------- | ------------ | ----------------------------------------- |
| `checks`         | `{}`         | `{name: callable}` readiness probes        |
| `version`        | `None`       | echoed by `/healthz` when set              |
| `liveness_path`  | `/healthz`   | liveness route                             |
| `readiness_path` | `/readyz`    | readiness route                            |
| `name`           | `"vitals"`   | blueprint name (change if registered twice)|

## 📡 Monitoring it (e.g. with Huginn)

Point an uptime monitor at each app:

- an **HTTP** monitor on `…/healthz` — expected status `200` → *is it alive?*
- a **keyword** monitor on `…/readyz` containing `"ready": true` → *is it serving?*

That's the UptimeRobot/Uptime-Kuma experience for any Flask app, with no bespoke
health code per service.

## 🛠️ Develop

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

## 🧱 Architecture

One module, `flask_vitals.blueprint`, exposing `vitals(...) -> flask.Blueprint`.
No global state, no dependency beyond Flask; readiness checks are injected by the
host app, so the library stays decoupled from your stack and trivially testable.

## 🤝 Contributing

Issues and PRs are welcome! Keep it small and tested:

1. `uv sync`
2. Make your change with a test.
3. `uv run ruff format . && uv run ruff check . && uv run mypy && uv run pytest`
4. Open a PR.

## 📄 License

[MIT](LICENSE) © Clara Vanacker
