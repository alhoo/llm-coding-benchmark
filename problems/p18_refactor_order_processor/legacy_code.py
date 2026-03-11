"""
LEGACY ORDER PROCESSOR - Poorly organized, duplicated logic, mixed concerns.
This file is provided as the starting point for refactoring.
DO NOT modify this file - produce a refactored solution that preserves behavior.
"""


def process_order(order_data):
    """
    Process an order: validate, calculate tax, calculate shipping, return result.
    Main entry point - refactored code must preserve this function signature and behavior.
    """
    # validation block 1 - check we have something
    if order_data is None:
        return {"success": False, "error": "order_data is required"}
    if not isinstance(order_data, dict):
        return {"success": False, "error": "order_data must be a dict"}

    # validation block 2 - required fields
    if "items" not in order_data:
        return {"success": False, "error": "items is required"}
    items = order_data.get("items")
    if not isinstance(items, list):
        return {"success": False, "error": "items must be a list"}
    if len(items) == 0:
        return {"success": False, "error": "items cannot be empty"}

    # validation block 3 - each item
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return {"success": False, "error": f"item {i} must be a dict"}
        if "price" not in it:
            return {"success": False, "error": f"item {i} missing price"}
        if "quantity" not in it:
            return {"success": False, "error": f"item {i} missing quantity"}
        p = it.get("price")
        q = it.get("quantity")
        if not isinstance(p, (int, float)):
            return {"success": False, "error": f"item {i} price must be number"}
        if not isinstance(q, int) or q < 1:
            return {"success": False, "error": f"item {i} quantity must be positive int"}

    # region - default to US
    region = order_data.get("region", "US")
    if not isinstance(region, str):
        return {"success": False, "error": "region must be a string"}
    region = region.upper()
    if region not in ("US", "EU", "CA"):
        return {"success": False, "error": "region must be US, EU, or CA"}

    # subtotal
    subtotal = 0.0
    for it in items:
        subtotal += it["price"] * it["quantity"]

    # TAX CALCULATION - US (duplicated pattern 1)
    if region == "US":
        tax_rate = 0.085
        taxable = 0.0
        for it in items:
            item_total = it["price"] * it["quantity"]
            if it.get("category") != "food":
                taxable += item_total
        tax = taxable * tax_rate

    # TAX CALCULATION - EU (duplicated pattern 2)
    elif region == "EU":
        tax_rate_std = 0.20
        tax_rate_red = 0.05
        tax = 0.0
        for it in items:
            item_total = it["price"] * it["quantity"]
            if it.get("category") == "books":
                tax += item_total * tax_rate_red
            else:
                tax += item_total * tax_rate_std

    # TAX CALCULATION - CA (duplicated pattern 3)
    elif region == "CA":
        tax_rate = 0.13
        tax = 0.0
        for it in items:
            item_total = it["price"] * it["quantity"]
            if it.get("category") != "groceries":
                tax += item_total * tax_rate

    # SHIPPING - mixed with validation
    shipping = 0.0
    ship_addr = order_data.get("shipping_address")
    if ship_addr is None:
        return {"success": False, "error": "shipping_address is required"}
    if not isinstance(ship_addr, dict):
        return {"success": False, "error": "shipping_address must be a dict"}
    if "country" not in ship_addr:
        return {"success": False, "error": "shipping_address.country is required"}
    country = str(ship_addr.get("country", "")).upper()

    if country == "US":
        if subtotal >= 100:
            shipping = 0
        elif subtotal >= 50:
            shipping = 5.99
        else:
            shipping = 9.99
    elif country == "CA":
        if subtotal >= 150:
            shipping = 0
        elif subtotal >= 75:
            shipping = 8.99
        else:
            shipping = 14.99
    else:
        if subtotal >= 200:
            shipping = 15.0
        else:
            shipping = 25.0

    # discount code - repeated if/elif pattern
    discount = 0.0
    code = order_data.get("discount_code")
    if code is not None and isinstance(code, str):
        code = code.strip().upper()
        if code == "SAVE10":
            discount = subtotal * 0.10
        elif code == "SAVE20":
            discount = subtotal * 0.20
        elif code == "FLAT5":
            discount = 5.0
        elif code == "FLAT15":
            discount = 15.0

    total = subtotal + tax + shipping - discount
    if total < 0:
        total = 0.0

    return {
        "success": True,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "discount": round(discount, 2),
        "total": round(total, 2),
    }


# =============================================================================
# BELOW: Additional legacy helpers with DUPLICATED patterns - same structure
# repeated with slight variations. Refactored solution should recognize and
# consolidate these into a single abstraction.
# =============================================================================

def _validate_order_structure(od):
    """Duplicate of validation logic - used by batch processor."""
    if od is None:
        return False, "order_data is required"
    if not isinstance(od, dict):
        return False, "order_data must be a dict"
    if "items" not in od:
        return False, "items is required"
    items = od.get("items")
    if not isinstance(items, list):
        return False, "items must be a list"
    if len(items) == 0:
        return False, "items cannot be empty"
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return False, f"item {i} must be a dict"
        if "price" not in it:
            return False, f"item {i} missing price"
        if "quantity" not in it:
            return False, f"item {i} missing quantity"
        if not isinstance(it.get("price"), (int, float)):
            return False, f"item {i} price must be number"
        q = it.get("quantity")
        if not isinstance(q, int) or q < 1:
            return False, f"item {i} quantity must be positive int"
    return True, None


def _compute_subtotal(items):
    """Simple helper - but same loop pattern repeated elsewhere."""
    st = 0.0
    for it in items:
        st += it["price"] * it["quantity"]
    return st


def _tax_us(items):
    """US tax - same logic as in process_order, duplicated."""
    rate = 0.085
    taxable = 0.0
    for it in items:
        tot = it["price"] * it["quantity"]
        if it.get("category") != "food":
            taxable += tot
    return taxable * rate


def _tax_eu(items):
    """EU tax - same logic as in process_order, duplicated."""
    std, red = 0.20, 0.05
    t = 0.0
    for it in items:
        tot = it["price"] * it["quantity"]
        if it.get("category") == "books":
            t += tot * red
        else:
            t += tot * std
    return t


def _tax_ca(items):
    """CA tax - same logic as in process_order, duplicated."""
    rate = 0.13
    t = 0.0
    for it in items:
        tot = it["price"] * it["quantity"]
        if it.get("category") != "groceries":
            t += tot * rate
    return t


def _shipping_us(subtotal):
    """US shipping - duplicated from process_order."""
    if subtotal >= 100:
        return 0
    if subtotal >= 50:
        return 5.99
    return 9.99


def _shipping_ca(subtotal):
    """CA shipping - duplicated from process_order."""
    if subtotal >= 150:
        return 0
    if subtotal >= 75:
        return 8.99
    return 14.99


def _shipping_intl(subtotal):
    """International shipping - duplicated from process_order."""
    return 15.0 if subtotal >= 200 else 25.0


def _apply_discount(code, subtotal):
    """Discount - same if/elif chain as in process_order."""
    if code is None or not isinstance(code, str):
        return 0.0
    code = code.strip().upper()
    if code == "SAVE10":
        return subtotal * 0.10
    if code == "SAVE20":
        return subtotal * 0.20
    if code == "FLAT5":
        return 5.0
    if code == "FLAT15":
        return 15.0
    return 0.0


def process_order_batch(orders):
    """
    Process multiple orders. Uses the duplicated helpers above.
    Refactored solution does NOT need to implement this - only process_order.
    This exists to demonstrate the scale of duplication in the codebase.
    """
    results = []
    for order in orders:
        ok, err = _validate_order_structure(order)
        if not ok:
            results.append({"success": False, "error": err})
            continue
        items = order["items"]
        region = order.get("region", "US").upper()
        if region not in ("US", "EU", "CA"):
            results.append({"success": False, "error": "region must be US, EU, or CA"})
            continue
        subtotal = _compute_subtotal(items)
        if region == "US":
            tax = _tax_us(items)
        elif region == "EU":
            tax = _tax_eu(items)
        else:
            tax = _tax_ca(items)
        ship_addr = order.get("shipping_address")
        if ship_addr is None or not isinstance(ship_addr, dict):
            results.append({"success": False, "error": "shipping_address is required"})
            continue
        country = str(ship_addr.get("country", "")).upper()
        if country == "US":
            shipping = _shipping_us(subtotal)
        elif country == "CA":
            shipping = _shipping_ca(subtotal)
        else:
            shipping = _shipping_intl(subtotal)
        discount = _apply_discount(order.get("discount_code"), subtotal)
        total = max(0, subtotal + tax + shipping - discount)
        results.append({
            "success": True,
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "shipping": round(shipping, 2),
            "discount": round(discount, 2),
            "total": round(total, 2),
        })
    return results
