"""Thin CLI wrapper so the validator runs without installing the package."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from er_dashboard.validate import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
