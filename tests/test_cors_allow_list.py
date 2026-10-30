"""
ST-43 (BLG-SEC-43, EPIC-06, v9.14) — per-environment CORS allow-list.

backend/config.py used one ALLOWED_ORIGINS list for every environment, so
production accepted credentialed cross-origin requests from
http://localhost:3000 and the staging frontend (allow_credentials=True,
allow_methods=["*"]). The list is now chosen per deployment:
CORS_ALLOWED_ORIGINS overrides; otherwise DEPLOY_ENV, or the Render
service it runs on, picks a documented default
(docs/infrastructure/cors_allow_list.md).

- AC 1: in production configuration a preflight from http://localhost:3000
  is rejected and one from the Pages origin is accepted.
- AC 2 (staging and production preflight checks on the deployed services)
  is post-merge, tracked by BLG-SEC-44.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

BACKEND = Path(__file__).parent.parent / "backend"
PAGES = "https://sachiv1984.github.io"
LOCALHOST = "http://localhost:3000"
STAGING_FRONTEND = "https://trading-assistant-staging.onrender.com"

# Render sets RENDER and RENDER_SERVICE_NAME on every service.
PRODUCTION_ENV = {"RENDER": "true", "RENDER_SERVICE_NAME": "trading-assistant-api"}
STAGING_ENV = {"RENDER": "true", "RENDER_SERVICE_NAME": "trading-assistant-api-staging"}


def _load_config():
    """A private copy of backend/config.py, so conftest's or another test's
    sys.modules["config"] stub is never involved."""
    spec = importlib.util.spec_from_file_location("config_real_for_test_cors", BACKEND / "config.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


config = _load_config()


def _app(origins):
    """An app with main.py's CORS settings and the given origins."""
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=["*"], allow_headers=["*"])

    @app.get("/positions")
    def positions():
        return {"ok": True}

    return TestClient(app)


def _preflight(client, origin):
    return client.options("/positions", headers={
        "Origin": origin,
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "x-api-key",
    })


class TestProductionPreflight:
    def setup_method(self):
        self.client = _app(config.resolve_allowed_origins(PRODUCTION_ENV))

    def test_localhost_is_rejected(self):
        resp = _preflight(self.client, LOCALHOST)
        assert resp.status_code == 400
        assert "access-control-allow-origin" not in resp.headers

    def test_staging_frontend_is_rejected(self):
        assert _preflight(self.client, STAGING_FRONTEND).status_code == 400

    def test_pages_origin_is_accepted(self):
        resp = _preflight(self.client, PAGES)
        assert resp.status_code == 200
        assert resp.headers["access-control-allow-origin"] == PAGES
        assert resp.headers["access-control-allow-credentials"] == "true"


class TestResolution:
    def test_render_service_without_staging_suffix_is_production(self):
        assert config.resolve_deploy_env(PRODUCTION_ENV) == "production"
        origins = config.resolve_allowed_origins(PRODUCTION_ENV)
        assert PAGES in origins and LOCALHOST not in origins and STAGING_FRONTEND not in origins

    def test_staging_service_gets_the_staging_frontend(self):
        assert config.resolve_deploy_env(STAGING_ENV) == "staging"
        origins = config.resolve_allowed_origins(STAGING_ENV)
        assert STAGING_FRONTEND in origins and PAGES not in origins

    def test_off_render_is_development(self):
        assert config.resolve_deploy_env({}) == "development"
        assert LOCALHOST in config.resolve_allowed_origins({})
        assert PAGES not in config.resolve_allowed_origins({})

    def test_deploy_env_wins_over_render_inference(self):
        env = dict(STAGING_ENV, DEPLOY_ENV="Production")
        assert config.resolve_deploy_env(env) == "production"

    def test_unknown_deploy_env_fails_loudly(self):
        with pytest.raises(ValueError, match="DEPLOY_ENV"):
            config.resolve_deploy_env({"DEPLOY_ENV": "prod"})

    def test_override_list_replaces_the_defaults(self):
        env = dict(PRODUCTION_ENV, CORS_ALLOWED_ORIGINS=f" {PAGES}/ , https://example.test ,")
        assert config.resolve_allowed_origins(env) == [PAGES, "https://example.test"]

    def test_blank_override_falls_back_to_the_defaults(self):
        env = dict(PRODUCTION_ENV, CORS_ALLOWED_ORIGINS=" , ")
        assert config.resolve_allowed_origins(env) == config.CORS_DEFAULT_ORIGINS["production"]


def test_module_level_list_follows_the_process_environment():
    """ALLOWED_ORIGINS itself (what main.py passes to CORSMiddleware) is
    resolved from the environment at import time."""
    code = ("import json, config; "
            "print(json.dumps({'env': config.DEPLOY_ENV, 'origins': config.ALLOWED_ORIGINS}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=BACKEND, capture_output=True, text=True,
                         env={"PATH": "/usr/bin:/bin", **PRODUCTION_ENV}, check=True)
    got = json.loads(out.stdout)
    assert got["env"] == "production"
    assert LOCALHOST not in got["origins"] and PAGES in got["origins"]


def test_main_passes_config_allowed_origins_to_cors_middleware():
    """main.py wires config.ALLOWED_ORIGINS into CORSMiddleware with
    credentials allowed, so the preflight results above are what the real
    app answers for the same list."""
    src = (BACKEND / "main.py").read_text()
    assert "allow_origins=ALLOWED_ORIGINS" in src
    assert "from config import (\n    API_TITLE,\n    ALLOWED_ORIGINS," in src
