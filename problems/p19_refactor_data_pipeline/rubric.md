# Evaluation Rubric: P19 - Refactor Data Transformation Pipeline

## Total Points: 100

---

## 1. Correctness (70 points)

The refactored `transform_records` must produce **identical output** to the legacy implementation.

| Category | Points | Description |
|----------|--------|-------------|
| Aggregation ops | 40 | sum, avg, count, min, max, concat all correct |
| Edge cases | 15 | Empty records, None values, non-numeric skip |
| Validation | 15 | All error cases return correct messages |

---

## 2. Pattern Recognition (20 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Unified aggregation | 10 | Strategy map or dispatcher, not six if/elif blocks |
| Extracted helpers | 10 | Validation + aggregation logic in separate functions |

---

## 3. Code Quality (10 points)

- Shared logic for numeric extraction (sum/avg/min/max all need numeric values)
- Clear separation of concerns

---

## Common LLM Failures

1. **Copy-paste**: Six if/elif blocks — fails pattern test
2. **Wrong count**: Counting all records vs. non-None values
3. **avg edge case**: Division by zero when no numeric values (should return 0)
4. **min/max empty**: Should return 0 when no values, not None
