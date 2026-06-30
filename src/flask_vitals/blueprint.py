"""A drop-in Flask health blueprint: ``/healthz`` (liveness) and ``/readyz``
(readiness).

Mirrors the liveness/readiness split that orchestrators and external monitors
(Huginn, UptimeRobot, Kubernetes…) expect:

* ``/healthz`` — the process is up. No dependencies probed. Always ``200``.
* ``/readyz`` — the app can serve: every registered check passes. ``200`` when
  all pass, ``503`` otherwise, with a per-check breakdown.

A check is any zero-arg callable. It passes unless it returns ``False`` or
raises — so ``lambda: db.session.execute(text("SELECT 1"))`` is a valid check.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING

from flask import Blueprint, jsonify

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

# A readiness check: a zero-arg callable. Healthy unless it returns False or
# raises (a None/truthy return passes).
type Check = Callable[[], object]


def vitals(
    *,
    checks: Mapping[str, Check] | None = None,
    version: str | None = None,
    liveness_path: str = "/healthz",
    readiness_path: str = "/readyz",
    name: str = "vitals",
) -> Blueprint:
    """Build a health blueprint. Register it: ``app.register_blueprint(vitals(...))``."""
    bp = Blueprint(name, __name__)
    registered = dict(checks or {})

    @bp.get(liveness_path)
    def liveness() -> ResponseReturnValue:
        body: dict[str, str] = {"status": "ok"}
        if version is not None:
            body["version"] = version
        return jsonify(body), 200

    @bp.get(readiness_path)
    def readiness() -> ResponseReturnValue:
        results: dict[str, bool] = {}
        all_ok = True
        for check_name, check in registered.items():
            try:
                passed = check() is not False  # None/truthy → pass
            except Exception:  # noqa: BLE001 - readiness must never raise
                passed = False
            results[check_name] = passed
            all_ok = all_ok and passed
        return jsonify({"ready": all_ok, "checks": results}), (200 if all_ok else 503)

    return bp
