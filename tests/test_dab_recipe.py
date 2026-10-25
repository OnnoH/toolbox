"""AC-2 of ONN-10: the example recipe and both of its plugins still run.

This needs dab/requirements.txt installed, which test_ci_contract.py does not,
so it has its own job (dab-recipe) in .github/workflows/checks.yml and the
ci-contract job skips this file. Collecting it without snowfakery is an error
on purpose: in the job that is meant to have it, a silent skip would hide the
very thing being checked.
"""

import csv
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
RECIPE = REPO / "dab" / "snowfakery" / "example.yaml"
RUNNER = REPO / "dab" / "run_recipe.py"


@pytest.fixture(scope="module")
def rows(tmp_path_factory):
    out = tmp_path_factory.mktemp("recipe")
    result = subprocess.run(
        [sys.executable, str(RUNNER), str(RECIPE),
         "--output-format=csv", f"--output-folder={out}"],
        capture_output=True, text=True, cwd=REPO,
    )
    assert result.returncode == 0, f"AC-2: the recipe failed\n{result.stderr}"
    csvs = sorted(out.glob("*.csv"))
    assert len(csvs) == 1, f"AC-2: expected one CSV, got {[p.name for p in csvs]}"
    with csvs[0].open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_ac2_the_recipe_writes_a_hundred_rows(rows):
    assert len(rows) == 100, f"AC-2: count: 100 in the recipe, got {len(rows)}"


def test_ac2_the_recipe_writes_the_four_recipe_fields(rows):
    assert set(rows[0]) >= {"NAME", "ADDRESS", "PHONE", "ACTIVE"}, (
        f"AC-2: columns are {sorted(rows[0])}"
    )


# random_string.RandomString, with fixed: false, draws its length from
# randrange(200), so one cell in 200 is legitimately empty: the check is the
# alphabet and the length, plus that the column is not empty wholesale.
RANDOM_STRING = {
    "NAME": re.compile(r"^[A-Z]?[a-z]*$"),     # case: CAPITALISE
    "ADDRESS": re.compile(r"^[A-Z]*$"),        # case: UPPER
    "PHONE": re.compile(r"^[0-9]*$"),          # case: NUMBERS
}


@pytest.mark.parametrize("field", sorted(RANDOM_STRING))
def test_ac2_random_string_fills_its_three_fields(rows, field):
    pattern = RANDOM_STRING[field]
    values = [row[field] for row in rows]
    wrong = [v for v in values if not pattern.match(v) or len(v) > 200]
    assert not wrong, f"AC-2: {field} not from RandomString: {wrong[:3]}"
    assert sum(1 for v in values if v) >= 90, (
        f"AC-2: {field} is empty in {sum(1 for v in values if not v)} of 100 rows"
    )


def test_ac2_faker_addons_fills_active(rows):
    """faker_addons.Provider.yes_no, reached through `fake: yes_no`."""
    wrong = sorted({row["ACTIVE"] for row in rows} - {"Y", "N"})
    assert not wrong, f"AC-2: ACTIVE is not yes_no: {wrong}"


def test_ac2_the_recipe_doc_runs_the_runner_not_the_console_script():
    """snowfakery's console script imports pkg_resources, which no setuptools
    that passes pip-audit still ships, so the recipe may not tell people to
    use it. Drop dab/run_recipe.py and go back to `snowfakery <recipe>` only
    when upstream has stopped importing pkg_resources.
    """
    doc = (REPO / "recipes" / "DataApiBuilder.md").read_text()
    shell = [line.strip() for line in doc.splitlines()
             if line.strip().startswith("snowfakery ")]
    assert not shell, f"AC-2: the doc still calls the console script: {shell}"
    assert "run_recipe.py" in doc, "AC-2: the doc does not mention the runner"
