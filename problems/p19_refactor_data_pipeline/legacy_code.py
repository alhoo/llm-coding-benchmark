"""
LEGACY DATA TRANSFORMATION PIPELINE - Poorly organized, repeated patterns.
Transforms records according to a schema with aggregation rules.
DO NOT modify this file - produce a refactored solution that preserves behavior.
"""


def transform_records(records, schema):
    """
    Transform a list of records according to schema. Schema defines which fields
    to aggregate and how. Main entry point - refactored code must preserve this.
    """
    if records is None:
        return {"success": False, "error": "records is required"}
    if not isinstance(records, list):
        return {"success": False, "error": "records must be a list"}
    if schema is None:
        return {"success": False, "error": "schema is required"}
    if not isinstance(schema, dict):
        return {"success": False, "error": "schema must be a dict"}

    if "aggregations" not in schema:
        return {"success": False, "error": "schema.aggregations is required"}
    aggs = schema["aggregations"]
    if not isinstance(aggs, list):
        return {"success": False, "error": "schema.aggregations must be a list"}

    for i, agg in enumerate(aggs):
        if not isinstance(agg, dict):
            return {"success": False, "error": f"aggregation {i} must be a dict"}
        if "field" not in agg:
            return {"success": False, "error": f"aggregation {i} missing field"}
        if "op" not in agg:
            return {"success": False, "error": f"aggregation {i} missing op"}
        op = agg.get("op")
        if op not in ("sum", "avg", "count", "min", "max", "concat"):
            return {"success": False, "error": f"aggregation {i} op must be sum, avg, count, min, max, or concat"}

    result = {}

    for agg in aggs:
        field = agg["field"]
        op = agg["op"]

        # SUM - first repeated pattern
        if op == "sum":
            total = 0
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    total += v
            result[field + "_sum"] = total

        # AVG - second repeated pattern (nearly identical to sum)
        elif op == "avg":
            total = 0
            cnt = 0
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    total += v
                    cnt += 1
            result[field + "_avg"] = round(total / cnt, 2) if cnt > 0 else 0

        # COUNT - third repeated pattern
        elif op == "count":
            cnt = 0
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is not None:
                    cnt += 1
            result[field + "_count"] = cnt

        # MIN - fourth repeated pattern
        elif op == "min":
            mn = None
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    if mn is None or v < mn:
                        mn = v
            result[field + "_min"] = mn if mn is not None else 0

        # MAX - fifth repeated pattern
        elif op == "max":
            mx = None
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    if mx is None or v > mx:
                        mx = v
            result[field + "_max"] = mx if mx is not None else 0

        # CONCAT - sixth pattern (different but same structure)
        elif op == "concat":
            parts = []
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                v = rec.get(field)
                if v is not None:
                    parts.append(str(v))
            sep = agg.get("separator", ",")
            result[field + "_concat"] = sep.join(parts)

    return {"success": True, "data": result}


# =============================================================================
# DUPLICATE: Same logic in a "batch" form - process multiple record sets
# =============================================================================

def _agg_sum(records, field):
    total = 0
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None and isinstance(v, (int, float)):
            total += v
    return total


def _agg_avg(records, field):
    total = 0
    cnt = 0
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None and isinstance(v, (int, float)):
            total += v
            cnt += 1
    return round(total / cnt, 2) if cnt > 0 else 0


def _agg_count(records, field):
    cnt = 0
    for rec in records:
        if not isinstance(rec, dict):
            continue
        if rec.get(field) is not None:
            cnt += 1
    return cnt


def _agg_min(records, field):
    mn = None
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None and isinstance(v, (int, float)):
            if mn is None or v < mn:
                mn = v
    return mn if mn is not None else 0


def _agg_max(records, field):
    mx = None
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None and isinstance(v, (int, float)):
            if mx is None or v > mx:
                mx = v
    return mx if mx is not None else 0


def _agg_concat(records, field, sep=","):
    parts = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        v = rec.get(field)
        if v is not None:
            parts.append(str(v))
    return sep.join(parts)


def transform_records_batch(record_sets, schema):
    """Batch version - demonstrates duplication. Refactored solution only needs transform_records."""
    results = []
    for records in record_sets:
        results.append(transform_records(records, schema))
    return results
