#!/usr/bin/env python3
"""
One-shot setup for the Shak Distributors store via the Shopify Admin REST API.

Creates everything automatically from the files in this repo:
  * 9 automated (smart) collections, tagged by category, with correct handles
  * 36 products from products_shak-distributors.csv
  * 6 pages from content/pages/*.html (About, Delivery, Shipping, Refund, Privacy, Contact)
  * Optional product images from data/images.json  ({ "product-handle": "https://image-url", ... })

It is SAFE TO RE-RUN: it skips anything whose handle already exists.

-------------------------------------------------------------------------------
HOW TO RUN (on any computer with internet — needs only Python 3, no pip installs):

  export SHOPIFY_STORE="your-store.myshopify.com"
  export SHOPIFY_TOKEN="shpat_xxxxxxxxxxxxxxxxxxxxx"
  python3 scripts/push_to_shopify.py

(Windows PowerShell:  $env:SHOPIFY_STORE="..." ; $env:SHOPIFY_TOKEN="..." ; python scripts/push_to_shopify.py)

Required Admin API scopes on the custom app: write_products, write_content.
You can uninstall/revoke the custom app as soon as this finishes.
-------------------------------------------------------------------------------
"""
import os, sys, csv, json, time, glob, re
import urllib.request, urllib.error

API_VERSION = "2024-04"
STORE = os.environ.get("SHOPIFY_STORE", "").replace("https://", "").replace("http://", "").strip("/")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORIES = [
    ("Apple Phones", "apple-phones"), ("Samsung", "samsung"), ("Oppo", "oppo"),
    ("Huawei", "huawei"), ("Tablets", "tablets"), ("Watches", "watches"),
    ("MacBooks", "macbooks"), ("Laptops", "laptops"), ("Accessories", "accessories"),
]

PAGES = [
    ("About Us", "about-us", "about-us.html", None),
    ("Delivery Policy", "delivery-policy", "delivery-policy.html", None),
    ("Shipping Terms", "shipping-terms", "shipping-terms.html", None),
    ("Refund Policy", "refund-policy", "refund-policy.html", None),
    ("Privacy Policy", "privacy-policy", "privacy-policy.html", None),
    ("Contact us", "contact", "contact.html", "contact"),
]


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def api(method, path, payload=None):
    url = f"https://{STORE}/admin/api/{API_VERSION}/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Shopify-Access-Token", TOKEN)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limited
                time.sleep(2 * (attempt + 1)); continue
            detail = e.read().decode()[:500]
            raise SystemExit(f"HTTP {e.code} on {method} {path}: {detail}")
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(2 ** attempt); continue
            die(f"Network error reaching {STORE}: {e}. "
                f"If you are on the restricted agent sandbox, run this script on a normal internet connection.")
    return {}


def strip_comment(html):
    return re.sub(r"^<!--.*?-->\s*", "", html, flags=re.DOTALL)


def main():
    if not STORE or not TOKEN:
        die("Set SHOPIFY_STORE and SHOPIFY_TOKEN environment variables first (see header of this file).")

    shop = api("GET", "shop.json").get("shop", {})
    print(f"Connected to: {shop.get('name')} ({shop.get('myshopify_domain')})  currency={shop.get('currency')}\n")

    # ---- Images map (optional) ----
    images = {}
    img_path = os.path.join(ROOT, "data", "images.json")
    if os.path.exists(img_path):
        images = json.load(open(img_path))
        print(f"Loaded {len(images)} image URLs from data/images.json\n")

    # ---- 1) Collections (smart collections, one rule: tag == category) ----
    existing_cols = {}
    page_info = "smart_collections.json?limit=250"
    for c in api("GET", page_info).get("smart_collections", []):
        existing_cols[c["handle"]] = c["id"]
    print("== Collections ==")
    for title, handle in CATEGORIES:
        if handle in existing_cols:
            print(f"  skip (exists): {title}")
            continue
        api("POST", "smart_collections.json", {"smart_collection": {
            "title": title, "handle": handle, "disjunctive": False,
            "rules": [{"column": "tag", "relation": "equals", "condition": title}],
            "published": True,
        }})
        print(f"  created: {title}  (/collections/{handle})")
        time.sleep(0.4)

    # ---- 2) Products from CSV ----
    existing_products = set()
    since = 0
    while True:
        batch = api("GET", f"products.json?limit=250&since_id={since}&fields=id,handle").get("products", [])
        if not batch:
            break
        for p in batch:
            existing_products.add(p["handle"]); since = p["id"]
        if len(batch) < 250:
            break
    print("\n== Products ==")
    csv_path = os.path.join(ROOT, "products_shak-distributors.csv")
    created = 0
    for row in csv.DictReader(open(csv_path, encoding="utf-8")):
        handle = row["Handle"]
        if handle in existing_products:
            print(f"  skip (exists): {row['Title']}"); continue
        variant = {
            "price": row["Variant Price"],
            "compare_at_price": row["Variant Compare At Price"] or None,
            "sku": row["Variant SKU"],
            "inventory_management": "shopify",
            "inventory_policy": row["Variant Inventory Policy"] or "deny",
            "inventory_quantity": int(row["Variant Inventory Qty"] or 0),
            "requires_shipping": row["Variant Requires Shipping"].upper() == "TRUE",
            "taxable": row["Variant Taxable"].upper() == "TRUE",
        }
        product = {
            "title": row["Title"], "handle": handle, "body_html": row["Body (HTML)"],
            "vendor": row["Vendor"], "product_type": row["Type"], "tags": row["Tags"],
            "status": row["Status"] or "active", "variants": [variant],
        }
        img = images.get(handle) or (row["Image Src"] or "").strip()
        if img:
            product["images"] = [{"src": img, "alt": row["Image Alt Text"]}]
        api("POST", "products.json", {"product": product})
        created += 1
        print(f"  created: {row['Title']}")
        time.sleep(0.5)
    print(f"  ({created} new products)")

    # ---- 3) Pages ----
    existing_pages = {p["handle"] for p in api("GET", "pages.json?limit=250&fields=handle").get("pages", [])}
    print("\n== Pages ==")
    for title, handle, fname, suffix in PAGES:
        if handle in existing_pages:
            print(f"  skip (exists): {title}"); continue
        html = strip_comment(open(os.path.join(ROOT, "content", "pages", fname), encoding="utf-8").read())
        body = {"title": title, "handle": handle, "body_html": html, "published": True}
        if suffix:
            body["template_suffix"] = suffix
        api("POST", "pages.json", {"page": body})
        print(f"  created: {title}  (/pages/{handle})")
        time.sleep(0.4)

    print("\nDone. Next: Online Store -> Navigation to build the header/footer menus,")
    print("then Themes -> Customize to publish. You can now uninstall the custom app.")


if __name__ == "__main__":
    main()
