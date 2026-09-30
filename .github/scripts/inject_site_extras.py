#!/usr/bin/env python3
"""Inline site extras (custom CSS + version switcher) into generated HTML pages.

Usage: inject_site_extras.py <site_dir> <custom_css> <switcher_js>
"""
import pathlib
import sys

CSS_MARKER = "meow-docs-custom"
JS_MARKER = "MeowVersionSwitcher"


def inject_before(text: str, closing: str, snippet: str) -> str:
    if closing in text:
        return text.replace(closing, snippet + closing, 1)
    return text + snippet


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2

    site = pathlib.Path(sys.argv[1])
    css_path = pathlib.Path(sys.argv[2])
    js_path = pathlib.Path(sys.argv[3])

    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1

    css = css_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8")

    style = f'\n<style id="{CSS_MARKER}">\n{css}\n</style>\n'
    script = "\n<script>\n" + js + "\n</script>\n"

    count = 0
    for html in site.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="ignore")
        changed = False
        if CSS_MARKER not in text:
            text = inject_before(text, "</head>", style)
            changed = True
        if JS_MARKER not in text:
            text = inject_before(text, "</body>", script)
            changed = True
        if changed:
            html.write_text(text, encoding="utf-8")
            count += 1

    print(f"injected site extras into {count} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
