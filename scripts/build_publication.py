#!/usr/bin/env python3
"""Build the publication and all human/machine interaction surfaces."""
from __future__ import annotations

import build_site
from apply_site_nav import main as apply_site_nav
from augment_site import augment
from fix_article_open_links import main as fix_article_open_links
from publish_failure_modes import main as publish_failure_modes
from publish_toolkit_assets import main as publish_toolkit_assets
from refine_agent_access import main as refine_agent_access
from refine_review_language import main as refine_review_language
from refine_webmcp_scope import main as refine_webmcp_scope


def main() -> None:
    build_site.build()
    fix_article_open_links()
    augment()
    publish_failure_modes()
    refine_webmcp_scope()
    publish_toolkit_assets()
    refine_agent_access()
    refine_review_language()
    apply_site_nav()


if __name__ == "__main__":
    main()
