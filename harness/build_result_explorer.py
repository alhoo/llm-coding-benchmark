"""
Build an interactive HTML result explorer for drilling down into benchmark results.

Drill-down hierarchy: Model -> Run -> Problem -> Details

Usage:
  python -m harness.build_result_explorer
  python -m harness.build_result_explorer --dir results -o result_explorer.html
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Truncate long strings to keep HTML manageable
MAX_OUTPUT_LEN = 4000
MAX_CODE_LEN = 15000


def load_result(path: Path) -> Optional[Dict]:
    """Load a single result JSON file."""
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def extract_model_from_filename(path: Path) -> str:
    """Extract model name from filename."""
    stem = path.stem
    match = re.match(r"^(.+?)_(?:python|javascript|java|cpp)_\d{8}_\d{6}$", stem)
    return match.group(1) if match else stem


def extract_run_id(path: Path) -> str:
    """Extract run timestamp from filename (e.g. 20260311_063727)."""
    stem = path.stem
    match = re.search(r"_(\d{8}_\d{6})$", stem)
    return match.group(1) if match else path.stem


def sanitize_problem_for_embed(problem: Dict[str, Any]) -> Dict[str, Any]:
    """Truncate long fields for embedding in HTML."""
    out = {
        "problem_id": problem.get("problem_id", "?"),
        "total_score": problem.get("total_score", 0),
        "code": problem.get("code", ""),
        "evaluation": problem.get("evaluation", {}),
    }
    if len(out["code"]) > MAX_CODE_LEN:
        out["code"] = out["code"][:MAX_CODE_LEN] + "\n# ... [truncated]"
    tr = out.get("evaluation", {}).get("test_results", {})
    if isinstance(tr.get("output"), str) and len(tr["output"]) > MAX_OUTPUT_LEN:
        out["evaluation"] = dict(out["evaluation"])
        out["evaluation"]["test_results"] = dict(tr)
        out["evaluation"]["test_results"]["output"] = (
            tr["output"][:MAX_OUTPUT_LEN] + "\n... [truncated]"
        )
    return out


def collect_runs(results_dir: Path) -> Dict[str, List[Dict]]:
    """
    Collect runs grouped by model.
    Returns: {model: [{run_id, timestamp, file, problems: [...]}, ...]}
    """
    model_runs: Dict[str, List[Dict]] = {}
    for path in results_dir.glob("*.json"):
        if "cache" in str(path):
            continue
        data = load_result(path)
        if not data:
            continue
        model = data.get("model") or extract_model_from_filename(path)
        run_id = extract_run_id(path)
        problems = [
            sanitize_problem_for_embed(p)
            for p in data.get("problems", [])
            if re.match(r"^p\d+_", p.get("problem_id", ""))
        ]
        run_info = {
            "run_id": run_id,
            "timestamp": data.get("timestamp", ""),
            "file": path.name,
            "problems": problems,
            "overall": data.get("overall", {}),
        }
        if model not in model_runs:
            model_runs[model] = []
        model_runs[model].append(run_info)
    # Sort runs by timestamp descending
    for model in model_runs:
        model_runs[model].sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return model_runs


def load_matrix(path: Path) -> tuple[Dict[str, Dict[str, float]], List[str], List[str]]:
    """Load matrix from CSV if it exists."""
    if not path.exists():
        return {}, [], []
    lines = path.read_text().strip().split("\n")
    if len(lines) < 2:
        return {}, [], []
    header = lines[0].split(",")
    models = [h.strip() for h in header[1:] if h.strip()]
    problems: List[str] = []
    matrix: Dict[str, Dict[str, float]] = {}
    for line in lines[1:]:
        parts = line.split(",")
        if not parts:
            continue
        problem_id = parts[0].strip()
        if not re.match(r"^p\d+_", problem_id):
            continue
        problems.append(problem_id)
        matrix[problem_id] = {}
        for i, model in enumerate(models):
            if i + 1 < len(parts) and parts[i + 1].strip():
                try:
                    matrix[problem_id][model] = float(parts[i + 1].strip())
                except ValueError:
                    pass
    return matrix, problems, models


def build_html(
    model_runs: Dict[str, List[Dict]],
    matrix: Dict[str, Dict[str, float]],
    problems: List[str],
    models: List[str],
) -> str:
    """Build the result explorer HTML with embedded data."""
    data_json = json.dumps({
        "model_runs": model_runs,
        "matrix": matrix,
        "problems": problems,
        "models": models,
    })
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Benchmark Result Explorer</title>
    <style>
        :root {{
            --bg: #0f0f12;
            --surface: #1a1a1f;
            --surface-hover: #24242c;
            --border: #2a2a35;
            --text: #e4e4e7;
            --text-muted: #a1a1aa;
            --accent: #6366f1;
            --accent-hover: #818cf8;
            --pass: #22c55e;
            --fail: #ef4444;
            --warn: #f59e0b;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 1.5rem;
            line-height: 1.5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text);
        }}
        .breadcrumb {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }}
        .breadcrumb a {{
            color: var(--accent);
            text-decoration: none;
        }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .breadcrumb span {{ color: var(--text-muted); margin: 0 0.25rem; }}
        .panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }}
        .panel-header {{
            padding: 0.75rem 1rem;
            background: var(--surface-hover);
            border-bottom: 1px solid var(--border);
            font-weight: 600;
        }}
        .list-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            transition: background 0.15s;
        }}
        .list-item:last-child {{ border-bottom: none; }}
        .list-item:hover {{ background: var(--surface-hover); }}
        .list-item .score {{
            font-weight: 600;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }}
        .score.pass {{ color: var(--pass); }}
        .score.fail {{ color: var(--fail); }}
        .score.partial {{ color: var(--warn); }}
        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .matrix-table th, .matrix-table td {{
            padding: 0.5rem 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        .matrix-table th {{
            background: var(--surface-hover);
            font-weight: 600;
        }}
        .matrix-table td.score-cell {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}
        .matrix-table td.score-cell.clickable {{
            cursor: pointer;
        }}
        .matrix-table td.score-cell.clickable:hover {{
            background: var(--surface-hover);
        }}
        .details-panel {{
            padding: 1rem;
        }}
        .details-panel pre {{
            background: var(--bg);
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.8rem;
            white-space: pre-wrap;
            word-break: break-all;
        }}
        .details-panel .section {{
            margin-bottom: 1.5rem;
        }}
        .details-panel .section-title {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
        }}
        .summary-stats {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }}
        .stat {{ color: var(--text-muted); font-size: 0.85rem; }}
        .stat strong {{ color: var(--text); }}
        .btn-back {{
            display: inline-block;
            padding: 0.4rem 0.8rem;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }}
        .btn-back:hover {{ background: var(--accent-hover); }}
        .view-matrix {{ margin-bottom: 1rem; }}
        .view-matrix a {{
            color: var(--accent);
            text-decoration: none;
        }}
        .view-matrix a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>LLM Benchmark Result Explorer</h1>
        <div id="breadcrumb" class="breadcrumb"></div>
        <div id="content"></div>
    </div>
    <script>
        const DATA = {data_json};

        const state = {{
            selectedCell: null,
            selectedRunIndex: null
        }};

        function scoreClass(score) {{
            if (score >= 90) return 'pass';
            if (score >= 60) return 'partial';
            return 'fail';
        }}

        function formatScore(score) {{
            return score != null ? score.toFixed(1) : '—';
        }}

        function getRunsForCell(problem, model) {{
            const runs = DATA.model_runs[model] || [];
            return runs.map((run, runIndex) => {{
                const pi = run.problems.findIndex(pr => pr.problem_id === problem);
                return pi >= 0 ? {{ runIndex, problemIndex: pi, run, problem: run.problems[pi] }} : null;
            }}).filter(Boolean);
        }}

        function renderBreadcrumb() {{
            let parts = ['<span>Matrix</span>'];
            if (state.selectedCell) {{
                parts.push('<span>/</span>');
                parts.push('<span>' + state.selectedCell.problem + ' × ' + state.selectedCell.model + '</span>');
            }}
            if (state.selectedCell && state.selectedRunIndex != null) {{
                const runs = getRunsForCell(state.selectedCell.problem, state.selectedCell.model);
                const r = runs[state.selectedRunIndex];
                if (r) parts.push('<span>/</span>', '<span>' + r.run.run_id + '</span>');
            }}
            document.getElementById('breadcrumb').innerHTML = parts.join('');
        }}

        function selectCell(problem, model) {{
            const runs = getRunsForCell(problem, model);
            if (runs.length === 0) return;
            state.selectedCell = {{ problem, model }};
            state.selectedRunIndex = runs.length === 1 ? 0 : null;
            render();
        }}

        function clearCell() {{
            state.selectedCell = null;
            state.selectedRunIndex = null;
            render();
        }}

        function selectRun(runIndex) {{
            state.selectedRunIndex = runIndex;
            render();
        }}

        function renderMatrix() {{
            let html = '<div class="panel"><div class="panel-header">Summary Matrix (problem × model)</div>';
            html += '<table class="matrix-table"><thead><tr><th>Problem</th>';
            for (const m of DATA.models) html += '<th>' + m + '</th>';
            html += '</tr></thead><tbody>';
            for (const p of DATA.problems) {{
                html += '<tr><td>' + p + '</td>';
                for (const m of DATA.models) {{
                    const v = DATA.matrix[p] && DATA.matrix[p][m];
                    const cls = v != null ? scoreClass(v) : '';
                    const runs = getRunsForCell(p, m);
                    const clickable = runs.length > 0 ? ' clickable' : '';
                    const onclick = runs.length > 0 ? ' onclick="selectCell(\\'' + p + '\\', \\'' + m + '\\')"' : '';
                    html += '<td class="score-cell ' + cls + clickable + '"' + onclick + '>' + formatScore(v) + '</td>';
                }}
                html += '</tr>';
            }}
            html += '</tbody></table></div>';
            return html;
        }}

        function renderRunsList() {{
            if (!state.selectedCell) return '';
            const {{ problem, model }} = state.selectedCell;
            const runs = getRunsForCell(problem, model);
            if (runs.length === 0) return '';
            let html = '<div class="panel"><div class="panel-header">Runs for ' + problem + ' × ' + model;
            html += ' <button class="btn-back" style="margin-left:1rem;padding:0.2rem 0.5rem;font-size:0.75rem" onclick="clearCell()">Clear</button></div>';
            runs.forEach((r, i) => {{
                const cls = scoreClass(r.problem.total_score);
                const sel = state.selectedRunIndex === i ? ' style="background:var(--surface-hover)"' : '';
                html += '<div class="list-item" onclick="selectRun(' + i + ')"' + sel + '>' +
                    '<span>' + r.run.run_id + '</span>' +
                    '<span class="score ' + cls + '">' + r.problem.total_score + '/100</span></div>';
            }});
            html += '</div>';
            return html;
        }}

        function renderDetails() {{
            if (!state.selectedCell || state.selectedRunIndex == null) return '';
            const runs = getRunsForCell(state.selectedCell.problem, state.selectedCell.model);
            const r = runs[state.selectedRunIndex];
            if (!r) return '';
            const p = r.problem;
            const ev = p.evaluation || {{}};
            const tr = ev.test_results || {{}};
            let html = '<div class="panel"><div class="panel-header">' + p.problem_id + ' — ' + r.run.run_id + ' — Score: ' + p.total_score + '/100</div>';
            html += '<div class="details-panel">';
            html += '<div class="section"><div class="section-title">Test Results</div>';
            html += '<div class="summary-stats">';
            html += `<span class="stat">Passed: <strong>${{tr.passed_tests ?? '?'}} / ${{tr.total_tests ?? '?'}}</strong></span>`;
            html += `<span class="stat">Status: <strong>${{tr.passed ? '✓ Pass' : '✗ Fail'}}</strong></span>`;
            html += '</div></div>';
            if (tr.output) {{
                html += '<div class="section"><div class="section-title">Test Output</div><pre>' + escapeHtml(tr.output) + '</pre></div>';
            }}
            html += '<div class="section"><div class="section-title">Generated Code</div><pre>' + escapeHtml(p.code || '(no code)') + '</pre></div>';
            html += '</div></div>';
            return html;
        }}

        function escapeHtml(s) {{
            if (!s) return '';
            const div = document.createElement('div');
            div.textContent = s;
            return div.innerHTML;
        }}

        function render() {{
            renderBreadcrumb();
            const content = document.getElementById('content');
            content.innerHTML = renderMatrix() + renderRunsList() + renderDetails();
        }}

        render();
    </script>
</body>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build interactive HTML result explorer"
    )
    parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path("results"),
        help="Results directory",
    )
    parser.add_argument(
        "--matrix", "-m",
        type=Path,
        help="Matrix CSV file (default: matrix.csv in project root)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("result_explorer.html"),
        help="Output HTML file",
    )
    args = parser.parse_args()

    results_dir = args.dir
    if not results_dir.is_dir():
        print(f"Error: Not a directory: {results_dir}", file=__import__("sys").stderr)
        return 1

    model_runs = collect_runs(results_dir)
    if not model_runs:
        print("No result files found.", file=__import__("sys").stderr)
        return 1

    matrix_path = args.matrix or Path("matrix.csv")
    matrix, problems, matrix_models = load_matrix(matrix_path)
    if not problems and not matrix_models:
        problems = sorted(set(
            p["problem_id"]
            for runs in model_runs.values()
            for run in runs
            for p in run["problems"]
        ))
        matrix_models = sorted(model_runs.keys())

    html = build_html(model_runs, matrix, problems, matrix_models)
    args.output.write_text(html)
    print(f"Result explorer written to {args.output}")
    return 0


if __name__ == "__main__":
    exit(main())
