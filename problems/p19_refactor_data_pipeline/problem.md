# Problem P19: Refactor Data Transformation Pipeline

## Problem Statement

You are given a **poorly organized legacy codebase** that transforms records according to an aggregation schema. Your task is to **refactor** it into clean, maintainable code while **preserving exact behavior**.

The legacy code exhibits:
- **Six nearly identical blocks**: sum, avg, count, min, max, concat — each iterates records, extracts a field, and applies one operation. The structure is the same; only the aggregation logic differs.
- **Repeated validation**: Schema validation mixed with transformation logic
- **Magic strings**: Output keys like `field_sum`, `field_avg` built by concatenation
- **No abstraction**: Each operation is a separate if/elif block with copy-pasted iteration

You must produce a **single Python file** that implements `transform_records(records: list, schema: dict) -> dict` with **identical behavior** to the legacy implementation.

---

## Required Interface

```python
def transform_records(records: list, schema: dict) -> dict:
    """
    Transform records according to schema.aggregations.
    Returns {"success": True, "data": {field_op: value, ...}}
    or {"success": False, "error": "..."} on validation failure.
    """
```

---

## Schema Format

```python
schema = {
    "aggregations": [
        {"field": "amount", "op": "sum"},
        {"field": "amount", "op": "avg"},
        {"field": "id", "op": "count"},
        {"field": "amount", "op": "min"},
        {"field": "amount", "op": "max"},
        {"field": "name", "op": "concat", "separator": ";"}  # separator optional, default ","
    ]
}
```

**Operations**: `sum`, `avg`, `count`, `min`, `max`, `concat`

- **sum/avg**: Only numeric values (int/float); skip None and non-numeric
- **count**: Count non-None values
- **min/max**: Only numeric; return 0 if no values; else min/max
- **concat**: Convert to string; join with separator (default ",")

---

## Legacy Codebase

The full legacy implementation is provided below. Recognize the repeated pattern: each operation iterates records, extracts `field`, filters/validates, then applies one aggregation. Refactor to a single abstraction (e.g., strategy map or dispatcher) that eliminates the six if/elif blocks.

---

## Refactoring Goals (Behavior Must Be Preserved)

1. **Unify aggregation logic** — one loop or one dispatcher per operation type
2. **Extract validation** — schema validation separate from transformation
3. **Eliminate duplication** — the six blocks share the same structure
4. **Use a strategy map** — op -> handler function

---

## Constraints

- **Single file output**: One Python file
- **No external dependencies**: Standard library only
- **Exact behavior**: All test cases must pass
- **Output keys**: `field_sum`, `field_avg`, `field_count`, `field_min`, `field_max`, `field_concat`
