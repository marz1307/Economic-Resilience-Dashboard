"""Validate the Economic Resilience Snapshot data assets.

Loads the three Excel files shipped under ``data/`` and asserts the dataset
descriptors quoted in the project README. Exits non-zero on any failure so
that CI surfaces a drift between the README and the data.
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

LOGGER = logging.getLogger("er_dashboard.validate")

# The eight core indicators the dashboard analyses.
CORE_INDICATORS: tuple[str, ...] = (
    "Gross domestic product, current prices,U.S. dollars",
    "Gross domestic product, constant prices,Percent change",
    "Inflation, end of period consumer prices,Percent change",
    "Unemployment rate,Percent of total labor force",
    "General government gross debt,Percent of GDP",
    "Current account balance,Percent of GDP",
    "Gross domestic product per capita, current prices,U.S. dollars",
    "Output gap in percent of potential GDP,Percent of potential GDP",
)

EXPECTED = {
    "raw_rows": 3893,
    "raw_indicator_columns": 44,
    "raw_country_count": 196,
    "year_min": 2001,
    "year_max": 2020,
    "year_span": 20,
    "complete_country_count": 26,
    "complete_observations": 520,  # 26 countries * 20 years
    "metadata_rows": 44,
    "core_indicators": 8,
}


@dataclass
class ValidationReport:
    """Outcome of a validation run."""

    passed: bool
    failures: list[str]
    summary: dict[str, object]


def _load(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data = pd.read_excel(data_dir / "data.xlsx", engine="openpyxl")
    groupings = pd.read_excel(data_dir / "country_groupings.xlsx", engine="openpyxl")
    metadata = pd.read_excel(data_dir / "metadata.xlsx", engine="openpyxl")
    return data, groupings, metadata


def validate(data_dir: Path) -> ValidationReport:
    """Run all checks and return a structured report."""

    data, groupings, metadata = _load(data_dir)
    failures: list[str] = []

    def check(label: str, actual: object, expected: object) -> None:
        if actual != expected:
            failures.append(f"{label}: expected {expected!r}, got {actual!r}")

    # Raw dataset shape.
    check("raw_rows", len(data), EXPECTED["raw_rows"])
    indicator_cols = [
        c
        for c in data.columns
        if c not in ("WEO Country Code", "ISO", "Country", "Year")
    ]
    check(
        "raw_indicator_columns",
        len(indicator_cols),
        EXPECTED["raw_indicator_columns"],
    )
    check(
        "raw_country_count",
        int(data["Country"].nunique()),
        EXPECTED["raw_country_count"],
    )
    check("year_min", int(data["Year"].min()), EXPECTED["year_min"])
    check("year_max", int(data["Year"].max()), EXPECTED["year_max"])
    check("year_span", int(data["Year"].nunique()), EXPECTED["year_span"])

    # Primary key integrity.
    pk_cols = ("ISO", "Country", "Year")
    for col in pk_cols:
        nulls = int(data[col].isna().sum())
        if nulls:
            failures.append(f"primary key column {col!r} contains {nulls} nulls")

    duplicates = int(data.duplicated(subset=["ISO", "Year"]).sum())
    if duplicates:
        failures.append(f"duplicate (ISO, Year) rows in raw dataset: {duplicates}")

    # Complete-case filter (the rule the dashboard applies in Power Query).
    missing_core = [c for c in CORE_INDICATORS if c not in data.columns]
    if missing_core:
        failures.append(f"core indicators missing from data: {missing_core}")
    else:
        complete = (
            data.dropna(subset=list(CORE_INDICATORS))
            .groupby("Country")["Year"]
            .nunique()
        )
        complete_countries = sorted(
            complete[complete == EXPECTED["year_span"]].index.tolist()
        )
        check(
            "complete_country_count",
            len(complete_countries),
            EXPECTED["complete_country_count"],
        )
        check(
            "complete_observations",
            len(complete_countries) * EXPECTED["year_span"],
            EXPECTED["complete_observations"],
        )

    # Country groupings sanity.
    if "Code" not in groupings.columns or "Region" not in groupings.columns:
        failures.append("country_groupings missing expected columns")
    else:
        gr_isos = set(groupings["Code"].dropna().astype(str))
        data_isos = set(data["ISO"].dropna().astype(str))
        unmatched = sorted(data_isos - gr_isos)
        # A few raw IMF ISO codes (e.g. UVK, WBG) are absent from the World
        # Bank classification list. They are filtered out before the
        # dashboard ingests the data so this is informational only.
        if unmatched:
            LOGGER.warning(
                "%d ISO codes in raw data have no grouping row "
                "(first 5: %s) - filtered out by dashboard load",
                len(unmatched),
                unmatched[:5],
            )

    # Metadata sanity.
    check("metadata_rows", len(metadata), EXPECTED["metadata_rows"])

    summary: dict[str, object] = {
        "raw_rows": int(len(data)),
        "raw_indicator_columns": len(indicator_cols),
        "raw_country_count": int(data["Country"].nunique()),
        "year_min": int(data["Year"].min()),
        "year_max": int(data["Year"].max()),
        "year_span": int(data["Year"].nunique()),
        "metadata_rows": int(len(metadata)),
        "core_indicators": len(CORE_INDICATORS),
    }

    return ValidationReport(passed=not failures, failures=failures, summary=summary)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing the three xlsx files (default: data).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    LOGGER.info("Validating data in %s", args.data_dir.resolve())
    report = validate(args.data_dir)

    LOGGER.info("Dataset summary:")
    for key, value in report.summary.items():
        LOGGER.info("  %s = %s", key, value)

    if report.passed:
        LOGGER.info("All %d checks passed.", len(EXPECTED))
        return 0

    LOGGER.error("Validation failed with %d issue(s):", len(report.failures))
    for line in report.failures:
        LOGGER.error("  - %s", line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
