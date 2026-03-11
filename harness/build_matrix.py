"""
Build a results matrix from multiple benchmark result files.

Matrix layout:
  - Rows = problem ID
  - Columns = model name
  - Cells = total_score (0-100)

Usage:
  python -m harness.build_matrix results/*.json
  python -m harness.build_matrix --dir results
  python -m harness.build_matrix --dir results -o matrix.csv
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def load_result(path: Path) -> Optional[Dict]:
    """Load a single result JSON file."""
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def extract_model_from_filename(path: Path) -> str:
    """Extract model name from filename like 'anomalia-122_python_20260311_063727.json'."""
    stem = path.stem
    match = re.match(r"^(.+?)_(?:python|javascript|java|cpp)_\d{8}_\d{6}$", stem)
    return match.group(1) if match else stem


def build_matrix(result_files: List[Path]) -> tuple[Dict[str, Dict[str, float]], List[str], List[str]]:
    """
    Build matrix from result files.
    Averages scores when multiple runs exist for the same problem+model.

    Returns:
        (matrix, problems, models)
        matrix: {problem_id: {model: avg_score}}
    """
    # Accumulate scores: {problem_id: {model: [scores]}}
    scores: Dict[str, Dict[str, List[int]]] = {}
    models: List[str] = []
    seen_models: set = set()

    for path in result_files:
        data = load_result(path)
        if not data:
            continue

        model = data.get("model") or extract_model_from_filename(path)
        if model not in seen_models:
            seen_models.add(model)
            models.append(model)

        for p in data.get("problems", []):
            problem_id = p.get("problem_id", "?")
            score = p.get("total_score", 0)
            if problem_id not in scores:
                scores[problem_id] = {}
            if model not in scores[problem_id]:
                scores[problem_id][model] = []
            scores[problem_id][model].append(score)

    # Average scores per (problem, model)
    matrix: Dict[str, Dict[str, float]] = {}
    for problem_id, model_scores in scores.items():
        matrix[problem_id] = {
            model: sum(vals) / len(vals)
            for model, vals in model_scores.items()
        }

    # Filter to valid problem IDs (p##_name)
    problems = sorted(p for p in matrix.keys() if re.match(r"^p\d+_", p))
    return matrix, problems, models


def _cell(value: float | str) -> str:
    """Format a cell value for display."""
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def format_markdown(matrix: Dict[str, Dict[str, float]], problems: List[str], models: List[str]) -> str:
    """Format matrix as Markdown table."""
    header = "| Problem | " + " | ".join(models) + " |"
    sep = "|--------|" + "|".join("---" for _ in models) + "|"
    rows = []
    for p in problems:
        cells = [_cell(matrix[p].get(m, "—")) for m in models]
        rows.append(f"| {p} | " + " | ".join(cells) + " |")
    return "\n".join([header, sep] + rows)


def format_csv(matrix: Dict[str, Dict[str, float]], problems: List[str], models: List[str]) -> str:
    """Format matrix as CSV."""
    header = "problem," + ",".join(models)
    rows = [header]
    for p in problems:
        cells = [_cell(matrix[p].get(m, "")) for m in models]
        rows.append(f"{p}," + ",".join(cells))
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Build a results matrix from multiple benchmark result files"
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Result JSON files",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        help="Directory containing result JSON files (excludes cache/)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file (default: stdout). Use .csv or .md extension.",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format (default: markdown)",
    )

    args = parser.parse_args()

    result_files: List[Path] = list(args.files)

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            parser.error(f"Not a directory: {args.dir}")
        for f in dir_path.glob("*.json"):
            if "cache" not in str(f):
                result_files.append(f)

    if not result_files:
        parser.error("No result files specified. Use files as args or --dir")

    matrix, problems, models = build_matrix(result_files)

    if not problems or not models:
        print("No data found in result files.", file=__import__("sys").stderr)
        return 1

    if args.format == "markdown":
        output = format_markdown(matrix, problems, models)
    else:
        output = format_csv(matrix, problems, models)

    if args.output:
        args.output.write_text(output)
        print(f"Matrix written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    exit(main())
