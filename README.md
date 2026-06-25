# Shak Distributors — Shopify Store

A complete, sleek **Online Store 2.0** Shopify theme plus ready-to-import content for a
phones / tablets / watches / laptops store (wholesale & retail, UK / GBP).

> **Brand:** Shak Distributors · **Tagline:** *Wholesale & Retail Tech — Dispatched in 1 Working Day* · **Currency:** GBP (£)

---

## What's in this repo

```
layout/      theme.liquid, password.liquid          → page shell
sections/    header, footer, hero, category-grid…    → all UI sections
snippets/    product-card, price, icons              → reusable bits
templates/   index, product, collection, page…       → OS 2.0 JSON templates
assets/      base.css, global.js                     → styling + cart JS
config/      settings_schema.json, settings_data.json→ theme settings (brand, colours, fonts)
locales/     en.default.json                         → text strings
products_shak-distributors.csv                       → 36 sample products (import this)
content/pages/*.html                                 → About + 4 policies + contact (paste-in)
data/generate_products.py                            → regenerates the CSV
```

---

## Step-by-step setup (≈20 min, no credentials shared with anyone)

### 1) Install the theme (via GitHub)
1. Push this repo to GitHub (already on branch `claude/shopify-electronics-store-us8eu7`).
2. In Shopify admin → **Online Store → Themes → Add theme → Connect from GitHub**.
3. Pick this repo + branch. Shopify imports it as an unpublished theme.
4. Click **Customize** to preview. Publish when you're happy.

*(Alternative: `zip` the repo contents and use Themes → Add theme → Upload zip, or use Shopify CLI `shopify theme push`.)*

### 2) Create the collections (these power the homepage)
Create **9 Automated collections** so products file themselves by tag.
For each: **Products → Collections → Create collection → Automated**, condition **`Product tag` is equal to `<Tag>`**.
The **handle must match exactly** (set it in the collection's *Search engine listing → Edit*):

| Collection title | Handle | Tag condition |
|---|---|---|
| Apple Phones | `apple-phones` | Product tag = `Apple Phones` |
| Samsung | `samsung` | Product tag = `Samsung` |
| Oppo | `oppo` | Product tag = `Oppo` |
| Huawei | `huawei` | Product tag = `Huawei` |
| Tablets | `tablets` | Product tag = `Tablets` |
| Watches | `watches` | Product tag = `Watches` |
| MacBooks | `macbooks` | Product tag = `MacBooks` |
| Laptops | `laptops` | Product tag = `Laptops` |
| Accessories | `accessories` | Product tag = `Accessories` |

### 3) Import the products
1. **Products → Import → Add file** → choose `products_shak-distributors.csv`.
2. Tick **Publish products** and import. 36 products load with descriptions, retail price,
   compare-at price, SKUs and stock (25 each). They auto-file into the collections above via tags.
3. **Add product photos** — the CSV ships without images (so it imports cleanly anywhere).
   Open each product and upload a photo, or add image URLs to the `Image Src` column before importing.
   Until then the theme shows a tidy placeholder.

### 4) Create the pages
For each file in `content/pages/`:
**Online Store → Pages → Add page**, set the **title** and (in the editor) switch to
**`<>` Show HTML** and paste the file contents. Use the handle shown in each file's top comment.

| File | Page title | Handle | Template |
|---|---|---|---|
| `about-us.html` | About Us | `about-us` | Default |
| `delivery-policy.html` | Delivery Policy | `delivery-policy` | Default |
| `shipping-terms.html` | Shipping Terms | `shipping-terms` | Default |
| `refund-policy.html` | Refund Policy | `refund-policy` | Default |
| `privacy-policy.html` | Privacy Policy | `privacy-policy` | Default |
| `contact.html` | Contact us | `contact` | **page.contact** |

> Shopify also has built-in policy fields (**Settings → Policies**) used at checkout — you can paste
> the refund & privacy content there too. The pages above are the customer-facing versions linked in the footer.

### 5) Build the navigation menus
**Online Store → Navigation.**
- **Main menu** (`main-menu`) — used by the header. Suggested:
  Home · Apple Phones · Samsung · Oppo · Huawei · Tablets · Watches · MacBooks · Laptops · Accessories
  (link each to its collection; group brands under a "Phones" parent if you like — the header supports one dropdown level).
- **Footer menus** — create a "Shop" menu (collections) and a "Policies" menu (the 5 pages). Then in
  **Customize → Footer**, point the footer blocks at these menus.

### 6) Finishing touches in Customize
- **Theme settings → Brand:** logo, favicon (brand name/tagline already set to *Shak Distributors*).
- **Theme settings → Colours:** accent defaults to a clean blue `#2563eb` — change to taste.
- **Header → Main menu:** select `main-menu`.
- Set the homepage **Hero** buttons and **Wholesale CTA** to point at `/collections/all` and `/pages/contact`.

---

## Wholesale pricing (optional enhancement)
Every product description already shows **Retail** and **Wholesale/trade** prices. To also show a
trade price in a highlighted box on the product page:
1. **Settings → Custom data → Products → Add definition**: name *Wholesale price*, namespace/key
   `custom.wholesale_price`, type **Money**.
2. Fill it in per product. The theme's product page renders it automatically when present.

For true B2B (separate logged-in trade pricing, net terms, min-order quantities), use Shopify's
**B2B / wholesale** features (Plus) or an app like *Wholesale Club* / *B2B Handsfree* later.

---

## Regenerate / edit the product list
Edit the `P = [...]` list in `data/generate_products.py`, then:
```bash
cd data && python3 generate_products.py
```
This rewrites `products_shak-distributors.csv`.

---

## Notes
- Prices are GBP and **illustrative samples** — review before going live.
- Policy pages are solid UK-focused starting points, not legal advice; have them reviewed for your business.
- Theme is responsive, accessible and dependency-free (vanilla CSS/JS).
