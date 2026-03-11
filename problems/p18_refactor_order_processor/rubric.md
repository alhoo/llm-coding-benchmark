# Evaluation Rubric: P18 - Refactor Order Processor

## Total Points: 100

---

## 1. Correctness (70 points)

The refactored `process_order` must produce **identical output** to the legacy implementation for all inputs.

| Category | Points | Description |
|----------|--------|-------------|
| Success cases | 35 | All valid orders produce correct subtotal, tax, shipping, discount, total |
| Validation errors | 25 | All error cases return correct error messages |
| Edge cases | 10 | Discount exceeding total, mixed categories, region defaults |

**Scoring**: Pass all test cases = 70 points. Each failed case reduces proportionally.

---

## 2. Pattern Recognition (20 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Extracted helpers | 10 | Validation, tax, shipping, discount in separate functions |
| No monolithic function | 10 | No single function > 80 lines (indicates copy-paste) |

---

## 3. Code Quality (10 points)

| Criterion | Points |
|-----------|--------|
| Named constants for rates/thresholds | 5 |
| Clear separation of concerns | 5 |

---

## Common LLM Failures

1. **Copy-paste**: Submitting legacy code with minimal changes — fails pattern tests
2. **Wrong tax logic**: Off-by-one in category checks (e.g., "food" vs "groceries")
3. **Rounding errors**: Using different rounding than legacy (round each field to 2 decimals)
4. **Validation order**: Missing checks or wrong error message text
