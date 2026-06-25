# 🚀 Shak Distributors — Go-Live Guide

Everything is built. There are **3 stages**. Stage 1 works from any device; Stages 2–3 are
where you choose **Route A (script, when you're at a computer)** or **Route B (no-code, in admin)**.

---

## Stage 1 — Install the theme (do this first, works on phone)

1. Shopify admin → **Online Store → Themes**.
2. **Add theme → Connect from GitHub** → pick repo **`Asadbashir1992/shopify-proj`**,
   branch **`claude/shopify-electronics-store-us8eu7`**.
3. It imports as a draft theme. Don't publish yet — publish after Stage 2 so the homepage has products to show.

---

## Stage 2 — Add products, collections & pages — pick ONE route

### ▶ Route A — One-command script (needs a computer with Python)

1. Get your token: app → **API credentials** tab → **Install app** → reveal **Admin API access token** (`shpat_…`).
   Scopes needed: `write_products`, `write_content`.
2. On a Mac/Windows/Linux computer:

   **Mac / Linux (Terminal):**
   ```bash
   git clone https://github.com/Asadbashir1992/shopify-proj.git
   cd shopify-proj && git checkout claude/shopify-electronics-store-us8eu7
   export SHOPIFY_STORE="your-store.myshopify.com"
   export SHOPIFY_TOKEN="shpat_paste_your_token_here"
   python3 scripts/push_to_shopify.py
   ```

   **Windows (PowerShell):**
   ```powershell
   git clone https://github.com/Asadbashir1992/shopify-proj.git
   cd shopify-proj ; git checkout claude/shopify-electronics-store-us8eu7
   $env:SHOPIFY_STORE="your-store.myshopify.com"
   $env:SHOPIFY_TOKEN="shpat_paste_your_token_here"
   python scripts/push_to_shopify.py
   ```
   *(No `git`? Download the repo as a ZIP from GitHub instead and `cd` into the folder.)*

3. It prints progress as it creates **9 collections, 36 products, 6 pages**. Safe to re-run.
4. When done, you can **uninstall the custom app** and rotate any exposed secret.

### ▶ Route B — No-code, in Shopify admin (no computer needed)

1. **Collections** — create 9 *Automated* collections (Products → Collections → Create → Automated),
   each with condition **Product tag = the name**, and set the handle to match:

   | Title | Handle | Tag |
   |---|---|---|
   | Apple Phones | `apple-phones` | `Apple Phones` |
   | Samsung | `samsung` | `Samsung` |
   | Oppo | `oppo` | `Oppo` |
   | Huawei | `huawei` | `Huawei` |
   | Tablets | `tablets` | `Tablets` |
   | Watches | `watches` | `Watches` |
   | MacBooks | `macbooks` | `MacBooks` |
   | Laptops | `laptops` | `Laptops` |
   | Accessories | `accessories` | `Accessories` |

2. **Products** — Products → Import → upload `products_shak-distributors.csv` → tick *Publish* → Import.
   (36 products auto-file into the collections via their tags.)
3. **Pages** — for each file in `content/pages/`, Online Store → Pages → Add page → set the title,
   switch the editor to **`<>` HTML**, paste the file. Set the Contact page's template to `page.contact`.

---

## Stage 3 — Menus & publish (both routes)

1. **Online Store → Navigation:**
   - **Main menu** → add: Home + each collection (Apple Phones, Samsung, Oppo, Huawei, Tablets, Watches, MacBooks, Laptops, Accessories).
   - Make a **Footer "Policies"** menu (the 5 policy pages) and a **Footer "Shop"** menu (collections).
2. **Themes → Customize:** set logo/favicon (Brand settings), point Footer blocks at your footer menus, tweak colours if you like.
3. **Publish** the theme. 🎉

---

## After go-live
- Replace placeholder product images: upload real photos per product, or edit URLs in `data/images.json`.
- Real contact details: edit the pages (currently placeholder email/phone).
- Review sample prices before taking live orders.
- Policies are solid UK starting points — have them reviewed for your business.
