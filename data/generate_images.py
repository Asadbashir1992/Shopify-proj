#!/usr/bin/env python3
"""Build data/images.json: handle -> image URL for every product.

Default: clean on-brand placeholder tiles (guaranteed to display, consistent look,
product name shown). Swap any value for a real photo URL and re-run the push script
(or re-run generate_products.py to bake URLs into the CSV) — both read this file.
"""
import csv, json, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "products_shak-distributors.csv")
OUT = os.path.join(ROOT, "data", "images.json")

# Theme-matched tile: light card background, dark text — sits cleanly on product cards.
BG = "f1f5f9"      # slate-100 (matches .product-card__media)
FG = "0f172a"      # slate-900 (matches body text)

def tile(title):
    label = urllib.parse.quote_plus(title)
    return f"https://placehold.co/800x800/{BG}/{FG}/png?text={label}"

images = {}
for row in csv.DictReader(open(CSV, encoding="utf-8")):
    images[row["Handle"]] = tile(row["Title"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(images, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"Wrote {len(images)} image URLs to {os.path.relpath(OUT, ROOT)}")
