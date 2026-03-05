#!/usr/bin/env python3
"""
Canada GIS Rebuilder
====================
Edit companies.csv, then run this script to regenerate the HTML.

Usage:
    python3 rebuild.py

Both files must be in the same folder as this script.
"""

import base64
import os
import sys
from datetime import datetime

# ── File paths (edit these if needed) ────────────────────────────────────────
CSV_FILE      = "canada_companies.csv"
TEMPLATE_FILE = "canada_gis_template.html"
OUTPUT_FILE   = "canada_postal_gis.html"
# ─────────────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_path      = os.path.join(script_dir, CSV_FILE)
    template_path = os.path.join(script_dir, TEMPLATE_FILE)
    output_path   = os.path.join(script_dir, OUTPUT_FILE)

    # ── Check files exist ─────────────────────────────────────────────────────
    for path, label in [(csv_path, CSV_FILE), (template_path, TEMPLATE_FILE)]:
        if not os.path.exists(path):
            print(f"ERROR: Cannot find '{label}' in {script_dir}")
            sys.exit(1)

    # ── Read and validate CSV ─────────────────────────────────────────────────
    with open(csv_path, "rb") as f:
        csv_bytes = f.read()

    csv_text  = csv_bytes.decode("utf-8")
    csv_lines = [l for l in csv_text.strip().split("\n") if l.strip()]
    row_count = len(csv_lines) - 1  # subtract header row

    if row_count < 1:
        print("ERROR: CSV appears empty or has only a header row.")
        sys.exit(1)

    headers = [h.strip() for h in csv_lines[0].split(",")]
    required = ["id", "name", "postal", "province", "city", "industry",
                "revenue_m", "employees", "founded", "status",
                "lat", "lng", "pop", "area_type"]
    missing = [h for h in required if h not in headers]
    if missing:
        print(f"WARNING: CSV is missing expected columns: {missing}")
        print("         The map may not display correctly.")

    print(f"CSV: {row_count} companies, {len(headers)} columns")

    # ── Encode CSV as base64 ──────────────────────────────────────────────────
    b64 = base64.b64encode(csv_bytes).decode("utf-8")
    print(f"Base64: {len(b64):,} characters")

    # ── Read template ─────────────────────────────────────────────────────────
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    if "%%CSVDATA%%" not in template:
        print(f"ERROR: Template file must contain the placeholder %%CSVDATA%%")
        sys.exit(1)

    # ── Inject and write ──────────────────────────────────────────────────────
    html = template.replace("%%CSVDATA%%", b64)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Output: {OUTPUT_FILE} ({size_kb:.0f} KB)")
    print(f"Built:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Done! Open canada_postal_gis.html in your browser.")


if __name__ == "__main__":
    main()
