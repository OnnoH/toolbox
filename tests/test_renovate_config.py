"""The acceptance criteria of ONN-27 ("renovate.json for OnnoH/toolbox"), as tests.

AC-1  The repo has a `renovate.json` at the root, matching the config the issue
      specifies: the Renovate schema, `config:recommended`, and one package rule
      that automerges minor, patch, pin and digest updates.
AC-2  `npx --package renovate renovate-config-validator renovate.json` exits 0.
AC-3  The checks that cover AC-1 and AC-2 run on every pull request, so "checks
      green" is a statement about these criteria and not only about ONN-8's.
AC-4  A change to the Renovate config leaves `.github/` alone: the board owns
      that directory as code owner.

Like the ONN-8 tests, the AC-2 tests come in a pair: one validates the config
in the repo, one validates a config with a planted mistake, so that a validator
that passes everything cannot make AC-2 look satisfied. Without npx they skip
rather than pass.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "renovate.json"
WORKFLOW = REPO / ".github" / "workflows" / "checks.yml"

# The config ONN-27 asks for, as the issue writes it.
EXPECTED = {
    "$schema": "https://docs.renovatebot.com/renovate-schema.json",
    "extends": ["config:recommended"],
    "packageRules": [
        {
            "description": (
                "Merge minor, patch, pin and digest updates once CI is green; "
                "majors wait for a maintainer."
            ),
            "matchUpdateTypes": ["minor", "patch", "pin", "digest"],
            "automerge": True,
        }
    ],
}

# Running the validator fetches the renovate package on the first call.
VALIDATOR_TIMEOUT = 900


def run_validator(*args, cwd):
    return subprocess.run(
        ["npx", "--yes", "--package", "renovate", "renovate-config-validator", *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
        timeout=VALIDATOR_TIMEOUT,
    )


# --------------------------------------------------------------------------
# AC-1: renovate.json at the root, as specified
# --------------------------------------------------------------------------


def test_ac1_config_is_at_the_repo_root():
    assert CONFIG.is_file(), "AC-1: no renovate.json at the root of the repo"


def test_ac1_config_matches_the_specified_config():
    assert json.loads(CONFIG.read_text(encoding="utf-8")) == EXPECTED


def test_ac1_automerge_rule_covers_the_four_update_types_and_no_more():
    rule = json.loads(CONFIG.read_text(encoding="utf-8"))["packageRules"][0]
    assert rule["automerge"] is True
    assert sorted(rule["matchUpdateTypes"]) == ["digest", "minor", "patch", "pin"]
    assert "major" not in rule["matchUpdateTypes"], (
        "AC-1: majors wait for a maintainer, so they may not automerge"
    )


# --------------------------------------------------------------------------
# AC-2: the config validator exits 0
# --------------------------------------------------------------------------


@pytest.mark.skipif(shutil.which("npx") is None, reason="no npx")
def test_ac2_validator_accepts_the_config():
    result = run_validator("renovate.json", cwd=REPO)
    assert result.returncode == 0, (
        f"AC-2: the validator rejected renovate.json:\n{result.stdout}{result.stderr}"
    )


@pytest.mark.skipif(shutil.which("npx") is None, reason="no npx")
def test_ac2_validator_rejects_a_config_with_a_mistake(tmp_path):
    """A validator that passes anything would make AC-2 meaningless."""
    broken = {"extends": ["config:recommended"], "packageRules": [{"automrge": True}]}
    (tmp_path / "renovate.json").write_text(json.dumps(broken), encoding="utf-8")
    result = run_validator("renovate.json", cwd=tmp_path)
    assert result.returncode != 0, "AC-2: the validator passed a misspelled option"


# --------------------------------------------------------------------------
# AC-3: these criteria are checked on every pull request
# --------------------------------------------------------------------------


@pytest.fixture(scope="module")
def workflow():
    with WORKFLOW.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_ac3_a_job_discovers_the_whole_tests_folder(workflow):
    """This file has to be picked up without naming it in the workflow."""
    runs = [
        str(step.get("run", ""))
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
    ]
    discovering = [run for run in runs if "pytest tests " in f"{run} "]
    assert discovering, "AC-3: no job runs pytest over the tests folder"
    assert not any(Path(__file__).name in run for run in runs), (
        "AC-3: the gate names this file instead of discovering it"
    )


def test_ac3_the_checks_run_on_pull_requests(workflow):
    # PyYAML reads an unquoted `on:` key as the boolean True.
    on = workflow.get("on", workflow.get(True))
    assert "pull_request" in on, "AC-3: the checks do not run on pull requests"


def test_ac3_this_file_is_not_excluded_from_the_run(workflow):
    ignored = [
        part
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        for part in str(step.get("run", "")).split()
        if part.startswith("--ignore")
    ]
    assert not any(Path(__file__).name in part for part in ignored), (
        f"AC-3: this file is ignored by the gate: {ignored}"
    )


# --------------------------------------------------------------------------
# AC-4: a Renovate change leaves .github/ alone
# --------------------------------------------------------------------------


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False, cwd=REPO
    )


def changed_against_main():
    """The paths this working tree changes relative to origin/main, or None.

    None when the base commit is not in the clone (a shallow checkout that
    cannot reach it): a missing base is a reason to skip, not to pass.
    """
    if git("rev-parse", "--verify", "--quiet", "origin/main").returncode != 0:
        if git("fetch", "--no-tags", "--depth=1", "origin", "main").returncode != 0:
            return None
        base = "FETCH_HEAD"
    else:
        base = "origin/main"
    merge_base = git("merge-base", base, "HEAD")
    if merge_base.returncode == 0:
        base = merge_base.stdout.strip()
    diff = git("diff", "--name-only", base, "HEAD")
    if diff.returncode != 0:
        return None
    return [line for line in diff.stdout.splitlines() if line]


def test_ac4_a_renovate_change_touches_nothing_under_github():
    changed = changed_against_main()
    if changed is None:
        pytest.skip("origin/main is not reachable from this checkout")
    if "renovate.json" not in changed:
        pytest.skip("this change does not touch renovate.json")
    offending = [path for path in changed if path.startswith(".github/")]
    assert not offending, (
        f"AC-4: the board owns .github/ as code owner; drop {offending} "
        "from this change and put it in its own pull request"
    )
