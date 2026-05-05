"""Run the validator against the shipped data and assert it succeeds."""

from __future__ import annotations

from pathlib import Path

from er_dashboard.validate import validate

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_dataset_descriptors_match_readme() -> None:
    report = validate(DATA_DIR)
    assert report.passed, "validation failures: " + "; ".join(report.failures)
    assert report.summary["raw_country_count"] == 196
    assert report.summary["year_span"] == 20
