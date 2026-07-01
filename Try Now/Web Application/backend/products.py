"""
products.py
Single source of truth for all products in FitAI.
Used by:
  - FastAPI backend  → /api/products endpoint
  - tryon.html frontend → product grid (loaded via fetch)
"""

PRODUCTS = [
    # ── Tops ──────────────────────────────────────────────────────────────────
    {
        "id":       "white_tee",
        "name":     "Classic White Tee",
        "category": "tops",
        "meta":     "Cotton · Regular fit",
        "price":    "Rs. 2,200",
        "badge":    "New",
        "badge_style": "rust",
        "img_file": "white_tee.jpg",
    },
    {
        "id":       "oxford_shirt",
        "name":     "Oxford Button-Down",
        "category": "tops",
        "meta":     "Sky Blue · Slim fit",
        "price":    "Rs. 5,500",
        "badge":    None,
        "img_file": "oxford_shirt.jpg",
    },
    {
        "id":       "denim_overshirt",
        "name":     "Denim Overshirt",
        "category": "tops",
        "meta":     "Indigo · Relaxed fit",
        "price":    "Rs. 6,800",
        "badge":    "Hot",
        "badge_style": "warm",
        "img_file": "denim_overshirt.jpg",
    },

    # ── Bottoms ────────────────────────────────────────────────────────────────
    {
        "id":       "slim_jeans",
        "name":     "Slim Fit Jeans",
        "category": "bottoms",
        "meta":     "Dark Indigo · Stretch",
        "price":    "Rs. 7,200",
        "badge":    None,
        "img_file": "slim_jeans.jpg",
    },
    {
        "id":       "khaki_chinos",
        "name":     "Khaki Chinos",
        "category": "bottoms",
        "meta":     "Tan · Tailored fit",
        "price":    "Rs. 5,900",
        "badge":    "New",
        "badge_style": "rust",
        "img_file": "khaki_chinos.jpg",
    },
    {
        "id":       "black_trousers",
        "name":     "Black Trousers",
        "category": "bottoms",
        "meta":     "Black · Straight leg",
        "price":    "Rs. 6,400",
        "badge":    None,
        "img_file": "black_trousers.jpg",
    },

    # ── Shoes ─────────────────────────────────────────────────────────────────
    {
        "id":       "white_sneakers",
        "name":     "White Sneakers",
        "category": "shoes",
        "meta":     "White · Low top",
        "price":    "Rs. 12,000",
        "badge":    "New",
        "badge_style": "rust",
        "img_file": "white_sneakers.jpg",
    },
    {
        "id":       "runners",
        "name":     "Performance Runners",
        "category": "shoes",
        "meta":     "Grey/Orange · Mesh",
        "price":    "Rs. 14,500",
        "badge":    None,
        "img_file": "runners.jpg",
    },
    {
        "id":       "chukka_boots",
        "name":     "Chukka Boots",
        "category": "shoes",
        "meta":     "Brown · Suede",
        "price":    "Rs. 16,800",
        "badge":    "Hot",
        "badge_style": "warm",
        "img_file": "chukka_boots.jpg",
    },

    # ── Caps ──────────────────────────────────────────────────────────────────
    {
        "id":       "baseball_cap",
        "name":     "Baseball Cap",
        "category": "caps",
        "meta":     "Navy · Adjustable",
        "price":    "Rs. 1,800",
        "badge":    None,
        "img_file": "baseball_cap.jpg",
    },
    {
        "id":       "snapback_cap",
        "name":     "Snapback Cap",
        "category": "caps",
        "meta":     "Black · One size",
        "price":    "Rs. 2,100",
        "badge":    None,
        "img_file": "snapback_cap.jpg",
    },
]

def get_product_by_id(product_id: str) -> dict | None:
    return next((p for p in PRODUCTS if p["id"] == product_id), None)