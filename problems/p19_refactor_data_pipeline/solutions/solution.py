"""
Refactored Data Transformation Pipeline - Unified aggregation pattern.
"""

from typing import List, Dict, Any, Callable, Optional


def _validate(schema: dict) -> Optional[str]:
    """Extract schema validation."""
    if schema is None:
        return "schema is required"
    if not isinstance(schema, dict):
        return "schema must be a dict"
    if "aggregations" not in schema:
        return "schema.aggregations is required"
    aggs = schema["aggregations"]
    if not isinstance(aggs, list):
        return "schema.aggregations must be a list"
    valid_ops = {"sum", "avg", "count", "min", "max", "concat"}
    for i, agg in enumerate(aggs):
        if not isinstance(agg, dict):
            return f"aggregation {i} must be a dict"
        if "field" not in agg:
            return f"aggregation {i} missing field"
        if "op" not in agg:
            return f"aggregation {i} missing op"
        if agg.get("op") not in valid_ops:
            return f"aggregation {i} op must be sum, avg, count, min, max, or concat"
    return None


def _get_numeric_values(records: List[dict], field: str) -> List[float]:
    """Shared: extract numeric values from records."""
    vals = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None and isinstance(v, (int, float)):
            vals.append(v)
    return vals


def _agg_sum(records: List[dict], field: str) -> float:
    return sum(_get_numeric_values(records, field))


def _agg_avg(records: List[dict], field: str) -> float:
    vals = _get_numeric_values(records, field)
    return round(sum(vals) / len(vals), 2) if vals else 0


def _agg_count(records: List[dict], field: str) -> int:
    return sum(1 for rec in records if isinstance(rec, dict) and rec.get(field) is not None)


def _agg_min(records: List[dict], field: str) -> float:
    vals = _get_numeric_values(records, field)
    return min(vals) if vals else 0


def _agg_max(records: List[dict], field: str) -> float:
    vals = _get_numeric_values(records, field)
    return max(vals) if vals else 0


def _agg_concat(records: List[dict], field: str, sep: str = ",") -> str:
    parts = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None:
            parts.append(str(v))
    return sep.join(parts)


def _aggregate(records: List[dict], field: str, op: str, agg: dict) -> Any:
    """Single dispatcher for all aggregation types."""
    handlers: Dict[str, Callable] = {
        "sum": lambda: _agg_sum(records, field),
        "avg": lambda: _agg_avg(records, field),
        "count": lambda: _agg_count(records, field),
        "min": lambda: _agg_min(records, field),
        "max": lambda: _agg_max(records, field),
        "concat": lambda: _agg_concat(records, field, agg.get("separator", ",")),
    }
    return handlers[op]()


def transform_records(records: list, schema: dict) -> dict:
    """Transform records according to schema. Preserves legacy behavior."""
    if records is None:
        return {"success": False, "error": "records is required"}
    if not isinstance(records, list):
        return {"success": False, "error": "records must be a list"}

    err = _validate(schema)
    if err:
        return {"success": False, "error": err}

    result = {}
    for agg in schema["aggregations"]:
        field = agg["field"]
        op = agg["op"]
        key = f"{field}_{op}"
        result[key] = _aggregate(records, field, op, agg)

    return {"success": True, "data": result}
