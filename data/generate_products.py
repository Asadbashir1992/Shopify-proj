#!/usr/bin/env python3
"""Generate a Shopify-import-ready products CSV for Shak Distributors.
Run: python3 generate_products.py  ->  ../products_shak-distributors.csv
Prices in GBP. Each product description shows RETAIL + WHOLESALE (trade) pricing.
Products are tagged by category; create automated collections that match each tag.
"""
import csv, os

# (collection_tag, vendor, title, type, retail, compare_at, wholesale, blurb, specs)
P = [
    # ---------- Apple Phones ----------
    ("Apple Phones", "Apple", "iPhone 15 Pro Max 256GB", "Smartphone", 1149.00, 1199.00, 1019.00,
     "The most advanced iPhone with a titanium design, A17 Pro chip and a 5x telephoto camera.",
     [("Display","6.7\" Super Retina XDR OLED"),("Chip","A17 Pro"),("Storage","256GB"),("Camera","48MP main + 12MP ultra-wide + 12MP 5x tele"),("Battery","Up to 29h video"),("Build","Titanium, USB-C")]),
    ("Apple Phones", "Apple", "iPhone 15 128GB", "Smartphone", 799.00, 849.00, 709.00,
     "iPhone 15 with Dynamic Island, a 48MP main camera and USB-C.",
     [("Display","6.1\" Super Retina XDR OLED"),("Chip","A16 Bionic"),("Storage","128GB"),("Camera","48MP main + 12MP ultra-wide"),("Battery","Up to 20h video"),("Build","Aluminium, USB-C")]),
    ("Apple Phones", "Apple", "iPhone 14 128GB", "Smartphone", 649.00, 699.00, 575.00,
     "Dependable everyday iPhone with great cameras and all-day battery.",
     [("Display","6.1\" Super Retina XDR OLED"),("Chip","A15 Bionic"),("Storage","128GB"),("Camera","12MP dual"),("Battery","Up to 20h video"),("Build","Aluminium, Lightning")]),
    ("Apple Phones", "Apple", "iPhone 13 128GB", "Smartphone", 529.00, 579.00, 469.00,
     "Excellent value flagship-class iPhone, ideal for trade volume.",
     [("Display","6.1\" Super Retina XDR OLED"),("Chip","A15 Bionic"),("Storage","128GB"),("Camera","12MP dual"),("Battery","Up to 19h video"),("Build","Aluminium, Lightning")]),

    # ---------- Samsung ----------
    ("Samsung", "Samsung", "Galaxy S24 Ultra 256GB", "Smartphone", 1099.00, 1249.00, 975.00,
     "Galaxy AI flagship with a built-in S Pen, titanium frame and 200MP camera.",
     [("Display","6.8\" QHD+ Dynamic AMOLED 2X 120Hz"),("Chip","Snapdragon 8 Gen 3"),("Storage","256GB"),("Camera","200MP + 50MP + 12MP + 10MP"),("Battery","5000mAh"),("Extras","S Pen, Galaxy AI")]),
    ("Samsung", "Samsung", "Galaxy S24 128GB", "Smartphone", 799.00, 899.00, 709.00,
     "Compact Galaxy AI flagship with a brilliant 120Hz display.",
     [("Display","6.2\" FHD+ AMOLED 120Hz"),("Chip","Exynos 2400"),("Storage","128GB"),("Camera","50MP + 12MP + 10MP"),("Battery","4000mAh"),("Extras","Galaxy AI")]),
    ("Samsung", "Samsung", "Galaxy A55 5G 128GB", "Smartphone", 399.00, 439.00, 349.00,
     "Best-selling mid-range 5G handset — a trade staple.",
     [("Display","6.6\" FHD+ Super AMOLED 120Hz"),("Chip","Exynos 1480"),("Storage","128GB"),("Camera","50MP + 12MP + 5MP"),("Battery","5000mAh"),("Build","Glass + metal frame")]),
    ("Samsung", "Samsung", "Galaxy Z Flip5 256GB", "Smartphone", 899.00, 1049.00, 799.00,
     "Foldable Galaxy with a large cover screen and pocketable design.",
     [("Display","6.7\" foldable AMOLED 120Hz + 3.4\" cover"),("Chip","Snapdragon 8 Gen 2"),("Storage","256GB"),("Camera","12MP + 12MP"),("Battery","3700mAh"),("Form","Clamshell fold")]),

    # ---------- Oppo ----------
    ("Oppo", "Oppo", "Find X7 Ultra 256GB", "Smartphone", 899.00, 999.00, 799.00,
     "Hasselblad quad-camera flagship with dual periscope zoom.",
     [("Display","6.82\" QHD+ AMOLED 120Hz"),("Chip","Snapdragon 8 Gen 3"),("Storage","256GB"),("Camera","Quad 50MP Hasselblad"),("Battery","5000mAh 100W"),("Extras","Dual periscope tele")]),
    ("Oppo", "Oppo", "Reno11 5G 256GB", "Smartphone", 399.00, 449.00, 349.00,
     "Sleek portrait-photography phone with fast 67W charging.",
     [("Display","6.7\" FHD+ AMOLED 120Hz"),("Chip","Dimensity 7050"),("Storage","256GB"),("Camera","50MP + 32MP tele + 8MP"),("Battery","4800mAh 67W"),("Build","Slim curved glass")]),
    ("Oppo", "Oppo", "Oppo A79 5G 128GB", "Smartphone", 219.00, 249.00, 189.00,
     "Affordable 5G with a big battery — strong wholesale margins.",
     [("Display","6.72\" FHD+ 90Hz"),("Chip","Dimensity 6020"),("Storage","128GB"),("Camera","50MP main"),("Battery","5000mAh 33W"),("Audio","Stereo speakers")]),
    ("Oppo", "Oppo", "Find N3 Flip 256GB", "Smartphone", 849.00, 999.00, 749.00,
     "Triple-camera flip foldable with a versatile cover display.",
     [("Display","6.8\" foldable AMOLED 120Hz"),("Chip","Dimensity 9200"),("Storage","256GB"),("Camera","50MP + 48MP + 32MP"),("Battery","4300mAh 44W"),("Form","Clamshell fold")]),

    # ---------- Huawei ----------
    ("Huawei", "Huawei", "Huawei P60 Pro 256GB", "Smartphone", 899.00, 1099.00, 799.00,
     "Ultra-lighting XMAGE camera system with a striking design.",
     [("Display","6.67\" LTPO OLED 120Hz"),("Chip","Snapdragon 8+ Gen 1 (4G)"),("Storage","256GB"),("Camera","48MP variable + 48MP tele + 13MP"),("Battery","4815mAh 88W"),("Note","No Google services")]),
    ("Huawei", "Huawei", "Huawei Mate 50 Pro 256GB", "Smartphone", 799.00, 949.00, 709.00,
     "Flagship with variable aperture camera and premium glass build.",
     [("Display","6.74\" OLED 120Hz"),("Chip","Snapdragon 8+ Gen 1 (4G)"),("Storage","256GB"),("Camera","50MP variable + 64MP tele + 13MP"),("Battery","4700mAh 66W"),("Note","No Google services")]),
    ("Huawei", "Huawei", "Huawei Nova 12 128GB", "Smartphone", 379.00, 429.00, 329.00,
     "Stylish mid-ranger with fast charging and a sharp selfie camera.",
     [("Display","6.7\" OLED 120Hz"),("Chip","Snapdragon 778G (4G)"),("Storage","128GB"),("Camera","50MP main + 60MP selfie"),("Battery","4600mAh 66W"),("Build","Slim glass")]),
    ("Huawei", "Huawei", "Huawei Mate X3 512GB", "Smartphone", 1799.00, 1999.00, 1599.00,
     "Ultra-thin book-style foldable flagship for premium customers.",
     [("Display","7.85\" foldable OLED + 6.4\" cover"),("Chip","Snapdragon 8+ Gen 1 (4G)"),("Storage","512GB"),("Camera","50MP + 13MP + 12MP tele"),("Battery","4800mAh 66W"),("Form","Book fold")]),

    # ---------- Tablets ----------
    ("Tablets", "Apple", "iPad Pro 11\" M4 256GB", "Tablet", 999.00, 1049.00, 889.00,
     "The thinnest Apple device ever with the blazing M4 chip and Ultra Retina XDR.",
     [("Display","11\" Ultra Retina XDR OLED 120Hz"),("Chip","Apple M4"),("Storage","256GB"),("Connectivity","Wi-Fi 6E"),("Accessory","Apple Pencil Pro support"),("Build","Aluminium, USB-C")]),
    ("Tablets", "Apple", "iPad Air 11\" M2 128GB", "Tablet", 599.00, 649.00, 529.00,
     "Powerful, portable iPad Air with the M2 chip for work and play.",
     [("Display","11\" Liquid Retina"),("Chip","Apple M2"),("Storage","128GB"),("Connectivity","Wi-Fi 6E"),("Accessory","Apple Pencil Pro support"),("Build","Aluminium, USB-C")]),
    ("Tablets", "Samsung", "Galaxy Tab S9 128GB", "Tablet", 649.00, 749.00, 575.00,
     "Premium AMOLED Android tablet with S Pen included and IP68 rating.",
     [("Display","11\" Dynamic AMOLED 2X 120Hz"),("Chip","Snapdragon 8 Gen 2"),("Storage","128GB"),("Extras","S Pen included, IP68"),("Battery","8400mAh"),("Audio","AKG quad speakers")]),
    ("Tablets", "Huawei", "Huawei MatePad 11.5\" 128GB", "Tablet", 329.00, 379.00, 289.00,
     "Great-value productivity tablet with a smooth 120Hz display.",
     [("Display","11.5\" IPS 120Hz"),("Chip","Snapdragon 7 Gen 1"),("Storage","128GB"),("Battery","7700mAh"),("Audio","Quad speakers"),("Note","No Google services")]),

    # ---------- Watches ----------
    ("Watches", "Apple", "Apple Watch Series 9 GPS 45mm", "Smartwatch", 429.00, 459.00, 379.00,
     "Brighter display, double-tap gesture and full health tracking.",
     [("Case","45mm aluminium"),("Display","Always-On Retina up to 2000 nits"),("Chip","S9 SiP"),("Health","ECG, blood oxygen, temperature"),("Battery","Up to 18h"),("Water","50m")]),
    ("Watches", "Apple", "Apple Watch Ultra 2 49mm", "Smartwatch", 799.00, 849.00, 709.00,
     "Rugged titanium adventure watch with the brightest Apple display.",
     [("Case","49mm titanium"),("Display","Always-On up to 3000 nits"),("Chip","S9 SiP"),("Health","ECG, depth gauge, dual-frequency GPS"),("Battery","Up to 36h"),("Water","100m, EN13319")]),
    ("Watches", "Samsung", "Galaxy Watch6 44mm", "Smartwatch", 289.00, 319.00, 249.00,
     "Slim Wear OS smartwatch with advanced sleep and body tracking.",
     [("Case","44mm aluminium"),("Display","1.5\" Super AMOLED"),("Chip","Exynos W930"),("Health","BIA, ECG, sleep coaching"),("Battery","425mAh"),("OS","Wear OS")]),
    ("Watches", "Huawei", "Huawei Watch GT4 46mm", "Smartwatch", 229.00, 259.00, 199.00,
     "Up to 14 days battery with elegant design and rich fitness tracking.",
     [("Case","46mm stainless steel"),("Display","1.43\" AMOLED"),("Health","TruSeen 5.5+, SpO2, sleep"),("Battery","Up to 14 days"),("GPS","Dual-band"),("Water","5ATM")]),

    # ---------- MacBooks ----------
    ("MacBooks", "Apple", "MacBook Air 13\" M3 256GB", "Laptop", 1099.00, 1149.00, 975.00,
     "Strikingly thin, fanless laptop with all-day battery and the M3 chip.",
     [("Display","13.6\" Liquid Retina"),("Chip","Apple M3 8-core"),("Memory","8GB unified"),("Storage","256GB SSD"),("Battery","Up to 18h"),("Ports","2x TB, MagSafe, headphone")]),
    ("MacBooks", "Apple", "MacBook Air 15\" M2 256GB", "Laptop", 1199.00, 1299.00, 1059.00,
     "Big-screen Air with spacious Liquid Retina display and silent design.",
     [("Display","15.3\" Liquid Retina"),("Chip","Apple M2 8-core"),("Memory","8GB unified"),("Storage","256GB SSD"),("Battery","Up to 18h"),("Audio","6-speaker system")]),
    ("MacBooks", "Apple", "MacBook Pro 14\" M3 512GB", "Laptop", 1699.00, 1799.00, 1519.00,
     "Pro performance with a stunning Liquid Retina XDR display.",
     [("Display","14.2\" Liquid Retina XDR 120Hz"),("Chip","Apple M3"),("Memory","8GB unified"),("Storage","512GB SSD"),("Battery","Up to 22h"),("Ports","3x TB4, HDMI, SDXC")]),
    ("MacBooks", "Apple", "MacBook Pro 16\" M3 Max 1TB", "Laptop", 3499.00, 3699.00, 3149.00,
     "The ultimate MacBook Pro for studios and power users.",
     [("Display","16.2\" Liquid Retina XDR 120Hz"),("Chip","Apple M3 Max"),("Memory","36GB unified"),("Storage","1TB SSD"),("Battery","Up to 22h"),("Ports","3x TB4, HDMI, SDXC")]),

    # ---------- Laptops ----------
    ("Laptops", "Dell", "Dell XPS 13 (i7, 16GB, 512GB)", "Laptop", 1299.00, 1399.00, 1149.00,
     "Premium ultraportable with an edge-to-edge InfinityEdge display.",
     [("Display","13.4\" FHD+ InfinityEdge"),("CPU","Intel Core i7"),("Memory","16GB"),("Storage","512GB SSD"),("Graphics","Intel Iris Xe"),("OS","Windows 11")]),
    ("Laptops", "HP", "HP Spectre x360 14 (i7, 16GB, 1TB)", "Laptop", 1399.00, 1499.00, 1249.00,
     "Convertible 2-in-1 with OLED touch display and premium build.",
     [("Display","14\" 2.8K OLED touch"),("CPU","Intel Core i7"),("Memory","16GB"),("Storage","1TB SSD"),("Form","2-in-1 convertible"),("OS","Windows 11")]),
    ("Laptops", "Lenovo", "Lenovo ThinkPad X1 Carbon G11", "Laptop", 1499.00, 1649.00, 1329.00,
     "Lightweight business flagship, MIL-SPEC tested and trade-favourite.",
     [("Display","14\" WUXGA IPS"),("CPU","Intel Core i7"),("Memory","16GB"),("Storage","512GB SSD"),("Weight","1.12kg"),("OS","Windows 11 Pro")]),
    ("Laptops", "ASUS", "ASUS Zenbook 14 OLED (i5, 16GB, 512GB)", "Laptop", 849.00, 949.00, 749.00,
     "Affordable OLED ultrabook with great battery and slim profile.",
     [("Display","14\" 2.8K OLED 90Hz"),("CPU","Intel Core i5"),("Memory","16GB"),("Storage","512GB SSD"),("Weight","1.28kg"),("OS","Windows 11")]),

    # ---------- Accessories ----------
    ("Accessories", "Apple", "AirPods Pro (2nd gen) USB-C", "Audio", 229.00, 249.00, 199.00,
     "Active Noise Cancellation, Adaptive Audio and USB-C charging case.",
     [("Type","In-ear ANC earbuds"),("Chip","Apple H2"),("Case","USB-C MagSafe"),("Battery","Up to 6h (30h w/ case)"),("Water","IP54"),("Extras","Adaptive Audio")]),
    ("Accessories", "Samsung", "Samsung 25W USB-C Fast Charger", "Charger", 19.99, 24.99, 12.50,
     "Genuine Samsung Super Fast Charging adapter — high-volume seller.",
     [("Output","25W USB-C PD PPS"),("Type","Mains adapter"),("Compatibility","Galaxy & USB-C PD devices"),("Safety","Over-current protection")]),
    ("Accessories", "Anker", "Anker 20,000mAh Power Bank 22.5W", "Power Bank", 39.99, 49.99, 27.50,
     "High-capacity power bank that charges phones and tablets fast.",
     [("Capacity","20,000mAh"),("Output","22.5W USB-C + USB-A"),("Recharge","USB-C in"),("Display","LED battery indicator"),("Safety","MultiProtect")]),
    ("Accessories", "Shak Distributors", "Braided USB-C to USB-C Cable 2m", "Cable", 9.99, 14.99, 4.50,
     "Durable 100W braided charging cable — perfect add-on / bulk buy.",
     [("Length","2m"),("Rating","100W / 5A"),("Data","480Mbps USB 2.0"),("Build","Nylon braided"),("Connector","USB-C to USB-C")]),
]

HEADERS = ["Handle","Title","Body (HTML)","Vendor","Type","Tags","Published",
           "Option1 Name","Option1 Value","Variant SKU","Variant Inventory Tracker",
           "Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service",
           "Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable",
           "Image Src","Image Alt Text","Gift Card","SEO Title","SEO Description","Status"]

def handle(title):
    h = title.lower()
    for ch in "()\"'.,/":
        h = h.replace(ch, "")
    h = h.replace("\\", "")
    return "-".join(h.split())

def body_html(blurb, retail, wholesale, specs):
    rows = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in specs)
    return (
        f"<p>{blurb}</p>"
        f"<table><tbody>{rows}</tbody></table>"
        f"<h3>Pricing</h3>"
        f"<ul>"
        f"<li><strong>Retail price:</strong> &pound;{retail:,.2f} inc. VAT</li>"
        f"<li><strong>Wholesale / trade price:</strong> &pound;{wholesale:,.2f} (minimum order quantities apply)</li>"
        f"</ul>"
        f"<p><em>Dispatched in 1 working day. Choose 48-hour express or 3&ndash;5 working day delivery at checkout. "
        f"Trade customers: <a href=\"/pages/contact\">contact us</a> for tiered pricing and a live stock list.</em></p>"
    )

def sku(tag, i):
    code = "".join(w[0] for w in tag.split())[:3].upper()
    return f"SHK-{code}-{i:03d}"

out_path = os.path.join(os.path.dirname(__file__), "..", "products_shak-distributors.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    for i, (tag, vendor, title, ptype, retail, compare, wholesale, blurb, specs) in enumerate(P, 1):
        tags = f"{tag}, {vendor}, {ptype}"
        w.writerow([
            handle(title), title, body_html(blurb, retail, wholesale, specs), vendor, ptype, tags, "TRUE",
            "Title", "Default Title", sku(tag, i), "shopify",
            25, "deny", "manual",
            f"{retail:.2f}", f"{compare:.2f}", "TRUE", "TRUE",
            "", title, "FALSE", f"{title} | Shak Distributors",
            blurb[:155], "active"
        ])
print(f"Wrote {len(P)} products to {os.path.normpath(out_path)}")
