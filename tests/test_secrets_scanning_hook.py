"""
ST-05 (BLG-SEC-22, EPIC-02, v7.10): Local secrets-scanning pre-commit gate.

Covers:
- .githooks/pre-commit invokes gitleaks against staged changes using the
  same .gitleaks.toml config as the CI-level gate (secret-scanning.yml,
  BLG-OPS-58).
- gitleaks (when installed) actually catches a deliberately-planted test
  secret staged in a scratch file, and the hook exits non-zero.
- A clean staging area passes (exit 0).

Skipped when `gitleaks` is not on PATH — this codebase's main "CI Pytest
Suite" job does not install gitleaks (only secret-scanning.yml, a separate
CI job, does), so this test is a local-dev/opt-in regression check rather
than a hard CI gate; the actual CI enforcement is secret-scanning.yml.

CI-safe: makes no network calls; only touches a scratch file in the repo's
own git index, which is reset before and after the test.
"""

import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOK_PATH = REPO_ROOT / ".githooks" / "pre-commit"
SCRATCH_FILE = REPO_ROOT / "zzz_test_secret_scratch.py"

_GITLEAKS_AVAILABLE = shutil.which("gitleaks") is not None


def _git(*args):
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)


@unittest.skipUnless(_GITLEAKS_AVAILABLE, "gitleaks not installed on PATH — install for local pre-commit enforcement")
class TestSecretsScanningPreCommitHook(unittest.TestCase):

    def tearDown(self):
        _git("reset", str(SCRATCH_FILE))
        if SCRATCH_FILE.exists():
            SCRATCH_FILE.unlink()

    def test_hook_exists_and_is_executable(self):
        self.assertTrue(HOOK_PATH.exists())
        self.assertTrue(HOOK_PATH.stat().st_mode & 0o111, "pre-commit hook must be executable")

    def test_hook_blocks_a_planted_secret(self):
        SCRATCH_FILE.write_text('GITHUB_TOKEN = "ghp_16C7e42F292c6912E7710c838347Ae178B4a"\n')
        _git("add", str(SCRATCH_FILE))
        result = subprocess.run(["bash", str(HOOK_PATH)], cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, "hook must reject a commit containing a planted secret")

    def test_hook_allows_a_clean_commit(self):
        SCRATCH_FILE.write_text("# nothing sensitive here\nVALUE = 42\n")
        _git("add", str(SCRATCH_FILE))
        result = subprocess.run(["bash", str(HOOK_PATH)], cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"hook must pass on a clean staging area; stderr: {result.stderr}")


if __name__ == "__main__":
    unittest.main()
