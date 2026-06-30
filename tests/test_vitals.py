"""Tests for the flask-vitals health blueprint."""

from __future__ import annotations

from typing import Any

from flask import Flask

from flask_vitals import vitals


def _app(**kwargs: Any) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(vitals(**kwargs))
    return app


def test_healthz_is_ok_with_version() -> None:
    client = _app(version="1.2.3").test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok", "version": "1.2.3"}


def test_healthz_omits_version_when_unset() -> None:
    resp = _app().test_client().get("/healthz")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}


def test_readyz_with_no_checks_is_ready() -> None:
    resp = _app().test_client().get("/readyz")
    assert resp.status_code == 200
    assert resp.json == {"ready": True, "checks": {}}


def test_readyz_reports_each_check_and_503_on_failure() -> None:
    def bad() -> None:
        raise RuntimeError("db down")

    def good() -> bool:
        return True

    client = _app(checks={"db": bad, "cache": good}).test_client()
    resp = client.get("/readyz")
    assert resp.status_code == 503
    assert resp.json == {"ready": False, "checks": {"db": False, "cache": True}}


def test_check_returning_false_fails() -> None:
    resp = _app(checks={"x": lambda: False}).test_client().get("/readyz")
    assert resp.status_code == 503


def test_check_returning_none_passes() -> None:
    resp = _app(checks={"x": lambda: None}).test_client().get("/readyz")
    assert resp.status_code == 200


def test_custom_paths() -> None:
    client = _app(liveness_path="/live", readiness_path="/ready").test_client()
    assert client.get("/live").status_code == 200
    assert client.get("/ready").status_code == 200
    assert client.get("/healthz").status_code == 404
