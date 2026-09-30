#!/usr/bin/env python3
"""Inline the version switcher script into every generated HTML page.

Usage: inject_version_switcher.py <site_dir> <switcher_js>
"""
import pathlib
import sys

MARKER = "MeowVersionSwitcher"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    site = pathlib.Path(sys.argv[1])
    switcher = pathlib.Path(sys.argv[2])

    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1

    js = switcher.read_text(encoding="utf-8")
    snippet = "\n<script>\n" + js + "\n</script>\n"

    count = 0
    for html in site.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="ignore")
        if MARKER in text:
            continue
        if "</body>" in text:
            text = text.replace("</body>", snippet + "</body>", 1)
        else:
            text = text + snippet
        html.write_text(text, encoding="utf-8")
        count += 1

    print(f"injected version switcher into {count} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
