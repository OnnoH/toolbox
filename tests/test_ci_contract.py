"""The acceptance criteria of ONN-8 ("Add CI checks to toolbox"), as tests.

AC-1  Per-language lint jobs, each failing independently on a lint error:
      shellcheck on bash/, ruff on python/ and dab/, ESLint on javascript/.
AC-2  A secret-scan job (gitleaks) runs on every push and pull request.
AC-3  A dependency-audit job runs pip-audit against dab/requirements.txt;
      no other language folder has a manifest to audit today.
AC-4  No single build job: the repo has no entry point to build.

The AC-1 tests come in pairs: one reads the workflow (the job exists, on its
own), one runs the linter on a file with a planted mistake (the job would
actually fail). Linters that are not installed skip rather than pass.
"""

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github" / "workflows" / "checks.yml"

with WORKFLOW.open(encoding="utf-8") as _handle:
    _WORKFLOW = yaml.safe_load(_handle)

# The tests run the linters at the versions the workflow pins, so that a bump
# in the workflow is a bump here too.
ESLINT_VERSION = _WORKFLOW["env"]["ESLINT_VERSION"]


@pytest.fixture(scope="module")
def workflow():
    return _WORKFLOW


@pytest.fixture(scope="module")
def jobs(workflow):
    return workflow["jobs"]


def job_script(job):
    """Everything the steps of one job run or use, as a single string."""
    parts = []
    for step in job.get("steps", []):
        parts.append(str(step.get("run", "")))
        parts.append(str(step.get("uses", "")))
    return "\n".join(parts)


def triggers(workflow):
    # PyYAML reads an unquoted `on:` key as the boolean True.
    return workflow.get("on", workflow.get(True))


# --------------------------------------------------------------------------
# AC-1: per-language lint jobs, each failing independently on a lint error
# --------------------------------------------------------------------------

LINT_JOBS = {
    "lint-bash": "shellcheck",
    "lint-python": "ruff",
    "lint-javascript": "eslint",
}


@pytest.mark.parametrize(("job_id", "tool"), sorted(LINT_JOBS.items()))
def test_ac1_lint_job_runs_its_tool(jobs, job_id, tool):
    assert job_id in jobs, f"AC-1: no {job_id} job in {WORKFLOW.name}"
    assert tool in job_script(jobs[job_id]), f"AC-1: {job_id} does not run {tool}"


@pytest.mark.parametrize("job_id", sorted(LINT_JOBS))
def test_ac1_lint_job_is_independent(jobs, job_id):
    """A failing lint job must not cancel or skip the other lint jobs."""
    assert "needs" not in jobs[job_id], f"AC-1: {job_id} waits on another job"


def test_ac1_bash_job_covers_the_bash_folder(jobs):
    script = job_script(jobs["lint-bash"])
    assert "'bash/*'" in script, "AC-1: lint-bash does not collect bash/"


def test_ac1_python_job_covers_python_and_dab(jobs):
    """Ruff runs over the whole tree, which is python/, dab/ and postman/."""
    script = job_script(jobs["lint-python"])
    assert "ruff check" in script and script.rstrip().endswith(".")
    assert (REPO / "ruff.toml").is_file(), "AC-1: ruff.toml pins the rule set"


def test_ac1_javascript_job_covers_the_js_files(jobs):
    script = job_script(jobs["lint-javascript"])
    assert "eslint" in script
    assert (REPO / "eslint.config.mjs").is_file(), "AC-1: no ESLint config"


@pytest.mark.skipif(shutil.which("shellcheck") is None, reason="no shellcheck")
def test_ac1_shellcheck_fails_on_a_lint_error(tmp_path):
    script = tmp_path / "broken.sh"
    script.write_text("#!/bin/bash\nif [ -z $1 ]\nthen\n  echo 'oops\nfi\n")
    result = subprocess.run(
        ["shellcheck", "--severity=warning", "--shell=bash", str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0, "AC-1: shellcheck passed a broken script"


@pytest.mark.skipif(shutil.which("ruff") is None, reason="no ruff")
def test_ac1_ruff_fails_on_a_lint_error(tmp_path):
    module = tmp_path / "broken.py"
    module.write_text("import os\n\nprint(undefined_name)\n")
    result = subprocess.run(
        ["ruff", "check", "--no-cache", "--config", str(REPO / "ruff.toml"), str(module)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0, "AC-1: ruff passed a broken module"
    assert "F821" in result.stdout, "AC-1: ruff rule set misses undefined names"


@pytest.mark.skipif(shutil.which("npx") is None, reason="no npx")
def test_ac1_eslint_fails_on_a_lint_error(tmp_path):
    # The config travels with the fixture: ESLint resolves its `files`
    # patterns relative to the directory the config sits in.
    shutil.copy(REPO / "eslint.config.mjs", tmp_path / "eslint.config.mjs")
    (tmp_path / "broken.js").write_text("const x = 1;\nconsole.log(typoed_name);\n")
    result = subprocess.run(
        ["npx", "--yes", f"eslint@{ESLINT_VERSION}", "broken.js"],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert result.returncode != 0, "AC-1: ESLint passed a broken script"
    assert "no-undef" in result.stdout, "AC-1: ESLint rule set misses no-undef"


# --------------------------------------------------------------------------
# AC-2: a secret-scan job (gitleaks) on every push and pull request
# --------------------------------------------------------------------------


def test_ac2_secret_scan_job_runs_gitleaks(jobs):
    assert "secret-scan" in jobs, "AC-2: no secret-scan job"
    assert "gitleaks" in job_script(jobs["secret-scan"]), "AC-2: not gitleaks"


def test_ac2_secret_scan_runs_on_push_and_pull_request(workflow):
    on = triggers(workflow)
    assert "push" in on, "AC-2: the workflow does not run on push"
    assert "pull_request" in on, "AC-2: the workflow does not run on PRs"
    # Unfiltered: AC-2 asks for *every* push, not only the ones to main.
    assert not on.get("push"), f"AC-2: push is filtered: {on.get('push')!r}"
    assert not on.get("pull_request"), "AC-2: pull_request is filtered"


def test_ac2_secret_scan_checks_the_whole_history(jobs):
    script = job_script(jobs["secret-scan"])
    assert "gitleaks dir" in script, "AC-2: the working tree is not scanned"
    assert "gitleaks git" in script, "AC-2: the history is not scanned"
    checkout = [s for s in jobs["secret-scan"]["steps"]
                if str(s.get("uses", "")).startswith("actions/checkout")]
    assert checkout and checkout[0].get("with", {}).get("fetch-depth") == 0, (
        "AC-2: a shallow checkout leaves most of the history unscanned"
    )


def test_ac2_gitleaks_download_is_pinned_and_verified(workflow):
    env = workflow["env"]
    assert env["GITLEAKS_VERSION"], "AC-2: gitleaks version not pinned"
    assert len(env["GITLEAKS_SHA256"]) == 64, "AC-2: no sha256 to verify"
    assert "sha256sum --check" in job_script(workflow["jobs"]["secret-scan"])


# --------------------------------------------------------------------------
# AC-3: a dependency audit over the one manifest in the repo
# --------------------------------------------------------------------------


def test_ac3_dependency_audit_runs_pip_audit_on_dab(jobs):
    assert "dependency-audit" in jobs, "AC-3: no dependency-audit job"
    script = job_script(jobs["dependency-audit"])
    assert "pip-audit" in script, "AC-3: the job does not run pip-audit"
    assert "dab/requirements.txt" in script, "AC-3: dab/ is not audited"


def test_ac3_every_python_manifest_is_audited(jobs):
    """Whatever pins Python dependencies has to be in the audit."""
    manifests = sorted(
        str(path.relative_to(REPO))
        for path in REPO.glob("**/requirements*.txt")
        if ".git" not in path.parts
    )
    assert "dab/requirements.txt" in manifests
    script = job_script(jobs["dependency-audit"])
    missing = [m for m in manifests if m not in script]
    assert not missing, f"AC-3: not audited: {missing}"


def test_ac3_dab_requirements_are_pinned(jobs):
    lines = [
        line.strip()
        for line in (REPO / "dab" / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert lines, "AC-3: dab/requirements.txt is empty"
    unpinned = [line for line in lines if "==" not in line]
    assert not unpinned, f"AC-3: an audit needs exact versions: {unpinned}"


def test_ac3_ignored_advisories_are_snowfakery_debt_only(jobs):
    """The ignore list exists only because snowfakery 3.x pins old packages.

    It may not outlive that pin: once snowfakery moves, the list has to go,
    or the audit would quietly keep passing over real advisories.
    """
    script = job_script(jobs["dependency-audit"])
    requirements = (REPO / "dab" / "requirements.txt").read_text()
    pinned_to_snowfakery_3 = "snowfakery==3." in requirements
    if not pinned_to_snowfakery_3:
        assert "--ignore-vuln" not in script, (
            "AC-3: snowfakery moved, so drop the ignored advisories"
        )
    # Ignoring whole packages or every advisory is not what this is for.
    assert "--ignore-vuln=*" not in script
    assert "--ignore" not in script.replace("--ignore-vuln", "")


def test_ac3_no_other_language_folder_has_a_manifest():
    """The reason the audit is Python-only. Add a job when this one fails."""
    others = sorted(
        str(path.relative_to(REPO))
        for pattern in ("**/package.json", "**/pom.xml", "**/build.gradle",
                        "**/Gemfile", "**/go.mod", "**/Cargo.toml")
        for path in REPO.glob(pattern)
        if ".git" not in path.parts and "node_modules" not in path.parts
    )
    assert not others, f"AC-3: these manifests need an audit job too: {others}"


# --------------------------------------------------------------------------
# AC-4: no single build job
# --------------------------------------------------------------------------


def test_ac4_there_is_no_build_job(jobs):
    """The toolbox is standalone scripts and notes: there is nothing to build."""
    build_jobs = [job_id for job_id in jobs if "build" in job_id.lower()]
    assert not build_jobs, f"AC-4: build is out of scope, found {build_jobs}"


def test_ac4_no_job_depends_on_another(jobs):
    """Without a build there is no stage to order the checks around."""
    chained = {job_id: job["needs"] for job_id, job in jobs.items() if "needs" in job}
    assert not chained, f"AC-4: the checks are not a pipeline: {chained}"
