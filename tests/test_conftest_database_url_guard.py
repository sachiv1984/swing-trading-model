"""
ST-14 (BLG-QA-188, EPIC-04, v9.7): the backend test suite must not connect to a real
database just because DATABASE_URL happens to already be set to one.

conftest.py's DATABASE_URL guard is exercised in a subprocess per test case (never in
this process, which has already imported conftest.py and set DATABASE_URL for the
whole session) -- each subprocess sets its own env, imports tests.conftest fresh, and
prints the resulting DATABASE_URL so this test can assert on it without disturbing the
running session's own environment.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

_SCRIPT = (
    "import os, sys\n"
    "sys.path.insert(0, '.')\n"
    "import tests.conftest\n"
    "print('DATABASE_URL=' + os.environ['DATABASE_URL'])\n"
)


def _run_isolated(env_overrides: dict) -> str:
    env = {"PATH": "/usr/bin:/bin"}
    env.update(env_overrides)
    result = subprocess.run(
        [sys.executable, "-c", _SCRIPT],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=60, env=env,
    )
    assert result.returncode == 0, (
        f"isolated conftest import failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    line = next(l for l in result.stdout.strip().splitlines() if l.startswith("DATABASE_URL="))
    return line.split("=", 1)[1]


class TestDatabaseUrlGuard:
    def test_real_looking_url_outside_ci_with_no_opt_in_is_overridden_to_stub(self):
        """The exact bug scenario: a real-looking DATABASE_URL set in a non-CI
        environment (e.g. this sandbox, configured with real staging credentials for
        unrelated interactive use), no PYTEST_ALLOW_REAL_DB opt-in, no CI env var --
        must be forced to the safe stub, not passed through."""
        url = _run_isolated({
            "DATABASE_URL": "postgresql://readonly_staging:x@db.example.supabase.co:5432/postgres",
        })
        assert "stub" in url.lower()
        assert "supabase" not in url

    def test_no_url_set_at_all_still_gets_the_stub(self):
        url = _run_isolated({})
        assert "stub" in url.lower()

    def test_ci_environment_passes_a_real_looking_url_through_unchanged(self):
        """Phase B CI (GitHub Actions sets CI=true automatically) must still be able
        to run tests/test_schema.py against its own real Postgres service container --
        no workflow file needs its own explicit opt-in var, since being in CI with an
        already-configured DATABASE_URL is itself the deliberate signal."""
        url = _run_isolated({
            "CI": "true",
            "DATABASE_URL": "postgresql://ci:ci@localhost:5432/ci_test",
        })
        assert url == "postgresql://ci:ci@localhost:5432/ci_test"

    def test_explicit_local_opt_in_passes_a_real_looking_url_through_unchanged(self):
        """A developer who has spun up their own throwaway Postgres and wants to run
        integration-style tests locally (not in CI) can opt in explicitly."""
        url = _run_isolated({
            "PYTEST_ALLOW_REAL_DB": "1",
            "DATABASE_URL": "postgresql://dev:dev@localhost:5433/my_local_pg",
        })
        assert url == "postgresql://dev:dev@localhost:5433/my_local_pg"

    def test_opt_in_var_alone_with_no_database_url_still_gets_the_stub(self):
        """PYTEST_ALLOW_REAL_DB=1 with no DATABASE_URL at all must not be treated as
        'deliberately configured' -- there is nothing to pass through, so the import-time
        ValueError guard still needs a value and the safe stub is used."""
        url = _run_isolated({"PYTEST_ALLOW_REAL_DB": "1"})
        assert "stub" in url.lower()
