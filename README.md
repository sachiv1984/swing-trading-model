# swing-trading-model
A model to help with swing trading.

## Local Development Setup

### Backend

The backend pins Python via `backend/.python-version` (currently `3.11.0`), matching CI (21 occurrences across 16 workflow files) and staging (`render.yaml`'s `PYTHON_VERSION: "3.11.0"`). Plain `python3 -m venv` does **not** read `.python-version` — it creates a venv against whatever `python3` resolves to on `PATH`, which silently drifts from the pin if your system Python is a different version. Use [`pyenv`](https://github.com/pyenv/pyenv) (or an equivalent version-manager shim that honours `.python-version`) so the pin is actually enforced:

```bash
cd backend
pyenv install $(cat .python-version)   # no-op if already installed
pyenv local $(cat .python-version)     # writes/confirms .python-version is picked up
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Verify the venv resolved to the pinned version before running anything:

```bash
backend/.venv/bin/python3 --version   # should print Python 3.11.0
```

Always invoke pytest via this venv, not the system Python — see `CLAUDE.md` §9 for why.

### Frontend

Standard `npm install` from the repo root; see `package.json` for scripts.
