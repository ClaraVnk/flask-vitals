# Contributing to flask-vitals

Thanks for your interest! This is a deliberately tiny library — contributions
that keep it small, typed and well-tested are very welcome.

## Setup

```bash
uv sync
```

## Before you open a PR

The CI runs exactly these — please run them locally first:

```bash
uv run ruff format --check .   # formatting
uv run ruff check .            # lint
uv run mypy                    # strict type check
uv run pytest                  # tests
```

## Guidelines

- **One intent per PR.** Small and focused beats big and sweeping.
- **Every change ships with a test.** Coverage of the public behaviour, not
  internals.
- **Keep the surface minimal.** New options need a clear, common use case — the
  point of the library is to stay boring and dependency-light (Flask only).
- **Conventional Commits** for messages (`feat:`, `fix:`, `docs:`, …).

## Reporting issues

Include the Flask version, a minimal reproduction, and what you expected vs. got.
