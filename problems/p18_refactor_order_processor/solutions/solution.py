"""
Refactored Order Processor - Clean separation of concerns, consolidated patterns.
"""

from typing import Optional

# Constants - no magic numbers
TAX_RATE_US = 0.085
TAX_RATE_EU_STD = 0.20
TAX_RATE_EU_REDUCED = 0.05
TAX_RATE_CA = 0.13

SHIPPING_US = [(100, 0), (50, 5.99), (0, 9.99)]
SHIPPING_CA = [(150, 0), (75, 8.99), (0, 14.99)]
SHIPPING_INTL = [(200, 15.0), (0, 25.0)]

DISCOUNTS = {
    "SAVE10": lambda s: s * 0.10,
    "SAVE20": lambda s: s * 0.20,
    "FLAT5": lambda s: 5.0,
    "FLAT15": lambda s: 15.0,
}


def _validate_order(order_data) -> Optional[str]:
    """Extract validation - single responsibility."""
    if order_data is None:
        return "order_data is required"
    if not isinstance(order_data, dict):
        return "order_data must be a dict"
    if "items" not in order_data:
        return "items is required"
    items = order_data.get("items")
    if not isinstance(items, list):
        return "items must be a list"
    if len(items) == 0:
        return "items cannot be empty"
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return f"item {i} must be a dict"
        if "price" not in it:
            return f"item {i} missing price"
        if "quantity" not in it:
            return f"item {i} missing quantity"
        if not isinstance(it.get("price"), (int, float)):
            return f"item {i} price must be number"
        q = it.get("quantity")
        if not isinstance(q, int) or q < 1:
            return f"item {i} quantity must be positive int"
    region = order_data.get("region", "US")
    if not isinstance(region, str):
        return "region must be a string"
    if region.upper() not in ("US", "EU", "CA"):
        return "region must be US, EU, or CA"
    ship_addr = order_data.get("shipping_address")
    if ship_addr is None:
        return "shipping_address is required"
    if not isinstance(ship_addr, dict):
        return "shipping_address must be a dict"
    if "country" not in ship_addr:
        return "shipping_address.country is required"
    return None


def _compute_subtotal(items) -> float:
    return sum(it["price"] * it["quantity"] for it in items)


def _compute_tax(items: list, region: str) -> float:
    """Consolidated tax calculation - single abstraction for all regions."""
    region = region.upper()
    if region == "US":
        taxable = sum(it["price"] * it["quantity"] for it in items if it.get("category") != "food")
        return taxable * TAX_RATE_US
    if region == "EU":
        return sum(
            it["price"] * it["quantity"] * (TAX_RATE_EU_REDUCED if it.get("category") == "books" else TAX_RATE_EU_STD)
            for it in items
        )
    # CA
    taxable = sum(it["price"] * it["quantity"] for it in items if it.get("category") != "groceries")
    return taxable * TAX_RATE_CA


def _compute_shipping(subtotal: float, country: str) -> float:
    """Consolidated shipping - threshold-based lookup."""
    country = country.upper()
    if country == "US":
        thresholds = SHIPPING_US
    elif country == "CA":
        thresholds = SHIPPING_CA
    else:
        thresholds = SHIPPING_INTL
    for min_subtotal, rate in thresholds:
        if subtotal >= min_subtotal:
            return rate
    return thresholds[-1][1]


def _compute_discount(code, subtotal: float) -> float:
    """Discount via lookup - no if/elif chain."""
    if code is None or not isinstance(code, str):
        return 0.0
    code = code.strip().upper()
    fn = DISCOUNTS.get(code)
    return fn(subtotal) if fn else 0.0


def process_order(order_data: dict) -> dict:
    """Process an order: validate, tax, shipping, discount. Preserves legacy behavior."""
    err = _validate_order(order_data)
    if err:
        return {"success": False, "error": err}

    items = order_data["items"]
    region = order_data.get("region", "US").upper()
    subtotal = _compute_subtotal(items)
    tax = _compute_tax(items, region)
    country = str(order_data["shipping_address"].get("country", "")).upper()
    shipping = _compute_shipping(subtotal, country)
    discount = _compute_discount(order_data.get("discount_code"), subtotal)
    total = max(0.0, subtotal + tax + shipping - discount)

    return {
        "success": True,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "discount": round(discount, 2),
        "total": round(total, 2),
    }
