"""flask-vitals — a drop-in Flask health blueprint (/healthz + /readyz)."""

from __future__ import annotations

from flask_vitals.blueprint import Check, vitals

__all__ = ["Check", "vitals"]
__version__ = "0.1.0"
