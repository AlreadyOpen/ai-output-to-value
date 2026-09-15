#!/usr/bin/env python3
"""Build the publication and all human/machine interaction surfaces."""
from __future__ import annotations

import build_site
from augment_site import augment
from publish_failure_modes import main as publish_failure_modes
from publish_toolkit_assets import main as publish_toolkit_assets


def main() -> None:
    build_site.build()
    augment()
    publish_failure_modes()
    publish_toolkit_assets()


if __name__ == "__main__":
    main()
