# Problem P18: Refactor Monolithic Order Processor

## Problem Statement

You are given a **poorly organized legacy codebase** that processes e-commerce orders. Your task is to **refactor** it into clean, maintainable code while **preserving exact behavior**.

The legacy code exhibits:
- **Duplicated logic**: Tax calculation repeated for US, EU, CA with nearly identical structure
- **Scattered validation**: Validation mixed with business logic, repeated in multiple places
- **Magic numbers and strings**: Hardcoded rates, thresholds, discount codes
- **Mixed concerns**: Validation, tax, shipping, and discount logic intertwined
- **Repeated patterns**: Same loop-and-accumulate pattern for subtotal, tax, shipping

You must produce a **single Python file** that implements `process_order(order_data: dict) -> dict` with **identical behavior** to the legacy implementation.

---

## Required Interface

Your refactored code **must** expose exactly:

```python
def process_order(order_data: dict) -> dict:
    """
    Process an order: validate, calculate tax, shipping, discount.
    Returns {"success": True, "subtotal": ..., "tax": ..., "shipping": ..., "discount": ..., "total": ...}
    or {"success": False, "error": "..."} on validation failure.
    """
```

---

## Legacy Codebase

The full legacy implementation is provided below. You only need to refactor and expose `process_order`—the batch processor and helpers demonstrate the scale of duplication.

Key behaviors to preserve:
- **Validation**: order_data (dict), items (non-empty list), each item: price (number), quantity (positive int), region US/EU/CA, shipping_address (dict with country)
- **Tax**: US 8.5% (exempt "food"), EU 20% std / 5% books, CA 13% (exempt "groceries")
- **Shipping**: US free ≥100 else 5.99≥50 else 9.99; CA free ≥150 else 8.99≥75 else 14.99; international 15≥200 else 25
- **Discount**: SAVE10=10%, SAVE20=20%, FLAT5=5, FLAT15=15

---

## Refactoring Goals (Behavior Must Be Preserved)

1. **Extract validation** into a clear, reusable validator (class or function)
2. **Consolidate tax calculation** — recognize the repeated pattern across US/EU/CA and unify
3. **Extract shipping logic** — same threshold-based structure for US, CA, international
4. **Extract discount logic** — replace if/elif chain with a lookup or strategy
5. **Eliminate magic numbers** — use named constants or configuration
6. **Reduce nesting** — early returns, guard clauses

---

## Constraints

- **Single file output**: Your solution must be one Python file
- **No external dependencies**: Use only the Python standard library
- **Exact behavior**: All test cases must pass; output must match legacy exactly
- **Backward compatible**: The `process_order` function signature and return structure are fixed

---

## Evaluation Criteria

1. **Correctness** (70 points) — All test cases pass; output matches legacy for every input
2. **Pattern Recognition** (20 points) — Tax/shipping/discount logic properly abstracted
3. **Code Quality** (10 points) — Readable, no magic numbers, clear separation of concerns
