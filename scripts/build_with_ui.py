#!/usr/bin/env python3
"""Build publication data, React/Tailwind UI assets, and pdfcn documents."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import build_publication

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(list(args), cwd=str(cwd or ROOT), check=True)


def main() -> None:
    build_publication.main()
    run("npm", "run", "build", cwd=WEB)
    run(sys.executable, str(ROOT / "scripts" / "inject_web_ui.py"))
    run("npm", "run", "pdf:meeting-brief", cwd=WEB)
    print("Built publication + shadcn/Base UI + Tailwind + pdfcn output")


if __name__ == "__main__":
    main()
