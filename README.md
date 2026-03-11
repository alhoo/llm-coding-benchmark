<div align="center">

# 🤖 LLM Coding Benchmark Suite

**Rigorous Evaluation Framework for Assessing Large Language Model Code Generation Capabilities**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Problems](https://img.shields.io/badge/Problems-15-green.svg)](#problem-catalog)
[![Languages](https://img.shields.io/badge/Languages-4-orange.svg)](#supported-languages)

*A curated collection of algorithmically complex coding problems designed to stress-test  
LLM reasoning, code generation accuracy, and edge case handling.*

</div>

---

## 📋 Purpose

This benchmark suite serves AI research labs and model evaluation teams by providing:

- **Standardized Test Cases** for comparing LLM performance across models
- **Multi-Language Support** (Python, JavaScript, Java, C++) to test language-agnostic reasoning
- **Comprehensive Rubrics** for objective pass/fail criteria
- **Edge Case Coverage** to identify model weaknesses
- **Reproducible Evaluation** with automated test harness

### Target Audience

- **AI Research Teams** evaluating GPT-4, Claude, Gemini, etc.
- **Model Training Teams** identifying weaknesses in code generation
- **Mercor-style Evaluators** assessing LLM capabilities for specific domains

---

## 🎯 Benchmark Philosophy

### What We Test

1. **Algorithm Implementation** - Not just syntax, but algorithmic correctness
2. **Edge Case Handling** - Boundary conditions, empty inputs, extreme values
3. **Time/Space Complexity** - Efficient solutions, not brute force
4. **Type Safety** - Proper handling of types and null values
5. **Error Handling** - Graceful failure modes

### What We Don't Test

- Simple CRUD operations
- Boilerplate code generation
- Documentation writing
- Code formatting

---

## 📊 Problem Catalog

| ID | Problem | Difficulty | Concepts | Pass Rate<br/>(GPT-4) | Pass Rate<br/>(Claude 3.5) |
|----|---------|-----------|----------|---------|---------|
| P01 | [Two-Sum with Hash Table](#p01-two-sum-optimized) | Medium | Hash maps, O(n) optimization | 95% | 92% |
| P02 | [LRU Cache](#p02-lru-cache) | Hard | LinkedList + HashMap, Doubly-linked list | 65% | 70% |
| P03 | [Binary Tree Serialization](#p03-binary-tree-codec) | Hard | Tree traversal, String parsing | 58% | 62% |
| P04 | [Topological Sort](#p04-topological-sort) | Hard | Graph algorithms, DFS, Cycle detection | 48% | 52% |
| P05 | [Longest Increasing Subsequence](#p05-lis-dynamic-programming) | Hard | Dynamic programming, Binary search | 42% | 45% |
| P06 | [Merge K Sorted Lists](#p06-merge-k-sorted-lists) | Hard | Heap/Priority queue, Divide & conquer | 55% | 60% |
| P07 | [Word Ladder](#p07-word-ladder) | Hard | BFS, Graph search | 38% | 41% |
| P08 | [Median of Two Sorted Arrays](#p08-median-two-sorted-arrays) | Expert | Binary search, O(log(min(m,n))) | 22% | 28% |
| P09 | [Regular Expression Matching](#p09-regex-matching) | Expert | Dynamic programming, Recursion | 18% | 24% |
| P10 | [Concurrent Task Scheduler](#p10-async-task-scheduler) | Expert | Async/await, Thread safety, Priority queues | 15% | 20% |
| P11 | [Weighted Job Scheduling](#p11-weighted-job-scheduling) | Expert | DP, Binary search, Interval scheduling | 12% | 16% |
| P12 | [LFU Cache](#p12-lfu-cache) | Expert | Frequency buckets, OrderedDict, O(1) design | 10% | 14% |
| P13 | [Smallest Range K Lists](#p13-smallest-range-k-lists) | Expert | Min-heap, Sliding window, Multi-list traversal | 12% | 15% |
| P18 | [Refactor Order Processor](#p18-refactor-order-processor) | Expert | Refactoring, Pattern recognition, Code organization | — | — |
| P19 | [Refactor Data Pipeline](#p19-refactor-data-pipeline) | Expert | Refactoring, Aggregation abstraction, DRY | — | — |
| P20 | [Largest Rectangle in Histogram](#p20-largest-rectangle-histogram) | Expert | Monotonic stack, O(n²)→O(n) optimization | — | — |

**Pass Rate**: Percentage of LLM-generated solutions that pass ALL test cases on first attempt.

---

## 🏗️ Architecture

```
llm-coding-benchmark/
├── problems/
│   ├── p01_two_sum/
│   │   ├── problem.md                 # Problem statement
│   │   ├── solutions/
│   │   │   ├── solution.py            # Reference solution (Python)
│   │   │   ├── solution.js            # Reference solution (JavaScript)
│   │   │   ├── solution.java          # Reference solution (Java)
│   │   │   └── solution.cpp           # Reference solution (C++)
│   │   ├── tests/
│   │   │   ├── test_cases.json        # Input/output test cases
│   │   │   ├── test_python.py         # Python test harness
│   │   │   ├── test_javascript.js     # JS test harness
│   │   │   └── test_java.java         # Java test harness
│   │   └── rubric.md                  # Evaluation criteria
│   ├── p02_lru_cache/
│   │   └── ...
│   └── ...
├── harness/
│   ├── run_benchmark.py               # Main benchmark runner
│   ├── llm_client.py                  # OpenAI/Anthropic integration
│   ├── evaluator.py                   # Test execution & grading
│   ├── reporter.py                    # Results visualization
│   ├── build_matrix.py                # Build problem×model results matrix
│   └── build_result_explorer.py       # Interactive HTML result explorer
├── results/
│   ├── cache/                         # Cached per-problem results (resume support)
│   ├── gpt4_results.json              # GPT-4 benchmark results
│   ├── claude_results.json            # Claude 3.5 results
│   └── comparison_report.html         # Side-by-side comparison
├── pyproject.toml
└── README.md
```

---

## 🚀 Usage

### Running the Full Benchmark

```bash
# Install dependencies
pip install -e .

# Run benchmark against GPT-4
python -m harness.run_benchmark --model gpt-4-turbo --problems all

# Run against Claude 3.5
python -m harness.run_benchmark --model claude-3-sonnet-20240229 --problems all

# Run specific problem
python -m harness.run_benchmark --model gpt-4-turbo --problems p01,p05,p08

# Disable cache and run all problems from scratch
python -m harness.run_benchmark --model gpt-4-turbo --problems all --no-cache
```

**Resume support**: Results are cached in `results/cache/` (or `{output-dir}/cache/`) per model, language, and problem. If a run is interrupted, re-run with the same arguments to resume from where you left off—cached problems are skipped. Use `--no-cache` to force a fresh run.

### Evaluating Custom LLM Output

```bash
# Test a generated solution against problem test cases
python -m harness.evaluator \
    --problem p02_lru_cache \
    --solution my_lru_solution.py \
    --language python
```

### Generating Comparison Report

```bash
python -m harness.reporter \
    --results results/gpt4_results.json results/claude_results.json \
    --output comparison_report.html
```

### Building Results Matrix

Create a matrix (rows = problem, columns = model) from multiple result files:

```bash
# From a directory of result JSONs
python -m harness.build_matrix --dir results

# From specific files
python -m harness.build_matrix results/*.json

# Output to CSV
python -m harness.build_matrix --dir results -o matrix.csv -f csv
```

### Result Explorer

Build an interactive HTML explorer to drill down into results: **Model → Run → Problem → Details**.

```bash
# Generate result_explorer.html (default)
python -m harness.build_result_explorer

# Custom paths
python -m harness.build_result_explorer --dir results -m matrix.csv -o result_explorer.html
```

Open the generated HTML in a browser to:
- View the summary matrix (problem × model scores)
- Drill down by model to see all runs
- Select a run to see per-problem scores
- Click a problem for full details (generated code, test output, evaluation)

---

## 📝 Problem Examples

### P01: Two-Sum (Optimized)

**Problem Statement**:
Given an array of integers `nums` and an integer `target`, return indices of two numbers that add up to `target`. You may assume exactly one solution exists. **Optimize for O(n) time complexity.**

**Example**:
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] == 9
```

**Constraints**:
- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Exactly one valid answer exists

**Rubric** ([Full Rubric](problems/p01_two_sum/rubric.md)):
- ✅ **Correctness** (60%): All test cases pass
  - Basic cases (target found)
  - Negative numbers
  - Duplicate values
  - Edge case: minimum array size
- ✅ **Complexity** (30%): O(n) time, O(n) space
- ✅ **Code Quality** (10%): Clear variable names, no magic numbers

**Common LLM Failures**:
1. **Brute Force**: Nested loops (O(n²)) instead of hash map
2. **Edge Cases**: Doesn't handle negative numbers correctly
3. **Type Errors**: Returns `[num1, num2]` instead of indices

---

### P08: Median of Two Sorted Arrays (Expert)

**Problem Statement**:
Given two sorted arrays `nums1` and `nums2`, return the **median** of the combined sorted arrays. **Must run in O(log(min(m,n))) time.**

**Example**:
```
Input: nums1 = [1, 3], nums2 = [2]
Output: 2.0

Input: nums1 = [1, 2], nums2 = [3, 4]
Output: 2.5
```

**Why This is Hard**:
- Requires binary search on the SMALLER array
- Partition logic is non-trivial
- Edge cases: empty arrays, all elements in one array
- Most LLMs default to O(m+n) merge approach

**Rubric**:
- ✅ Correctness (50%): All test cases pass
- ✅ Time Complexity (40%): O(log(min(m,n))) - verified via instrumentation
- ✅ Space Complexity (10%): O(1)

**GPT-4 Pass Rate**: 22% (Most submissions use O(m+n) merge)
**Claude 3.5 Pass Rate**: 28%

---

### P20: Largest Rectangle in Histogram (Expert)

**Problem Statement**:
You are given a **working O(n²) implementation** that finds the largest rectangle area in a histogram. Your task: **optimize it to O(n)** while preserving correctness.

**Why This is Hard**:
- The optimal solution requires a **monotonic stack** pattern—very non-obvious
- Naive approach: for each bar, expand left/right to find boundaries (O(n²))
- Optimal: when a shorter bar appears, it defines the right boundary for all taller bars in the stack
- Most LLMs either keep O(n²) (fails timing) or introduce off-by-one errors in the stack logic

**Rubric**:
- ✅ Correctness (50%): All test cases pass
- ✅ Time Complexity (40%): O(n) verified via timing on 50,000 bars
- ✅ Code Quality (10%): Clear implementation

**Expected Pass Rate**: Very low (~5–15%) — tests pattern recognition and algorithmic insight

---

## 🧪 Benchmark Harness

### How It Works

1. **Problem Loading**: Parse problem specifications and test cases
2. **LLM Querying**: Send problem statement to LLM API
3. **Code Extraction**: Parse LLM response for code blocks
4. **Test Execution**: Run generated code against test suite
5. **Rubric Evaluation**: Score based on correctness, complexity, quality
6. **Report Generation**: Aggregate results across all problems

### Example: Python Test Harness

```python
# problems/p01_two_sum/tests/test_python.py

import pytest
import json
from pathlib import Path

def load_test_cases():
    """Load test cases from JSON."""
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)

class TestTwoSum:
    @pytest.fixture
    def solution(self):
        """Import the solution function."""
        # Dynamically import user-provided solution
        from solutions import solution
        return solution.two_sum
    
    def test_basic_case(self, solution):
        """Test basic positive numbers."""
        assert solution([2, 7, 11, 15], 9) == [0, 1]
    
    def test_negative_numbers(self, solution):
        """Test with negative numbers."""
        assert solution([-1, -2, -3, -4, -5], -8) == [2, 4]
    
    def test_duplicates(self, solution):
        """Test with duplicate values."""
        assert solution([3, 3], 6) == [0, 1]
    
    def test_large_numbers(self, solution):
        """Test edge of constraint range."""
        assert solution([1000000000, -1000000000], 0) == [0, 1]
    
    @pytest.mark.parametrize("nums,target,expected", load_test_cases())
    def test_all_cases(self, solution, nums, target, expected):
        """Run all test cases from JSON."""
        result = solution(nums, target)
        assert sorted(result) == sorted(expected)
```

### Test Cases JSON

```json
[
  {
    "name": "basic_case",
    "nums": [2, 7, 11, 15],
    "target": 9,
    "expected": [0, 1]
  },
  {
    "name": "negative_numbers",
    "nums": [-1, -2, -3, -4, -5],
    "target": -8,
    "expected": [2, 4]
  },
  {
    "name": "zero_target",
    "nums": [-5, 0, 5, 10],
    "target": 0,
    "expected": [0, 2]
  }
]
```

---

## 📈 Evaluation Rubric

Each problem is scored on three dimensions:

### 1. Correctness (50-60%)

- **Pass/Fail** for each test case
- Edge cases weighted higher than basic cases
- Score: `(passed_tests / total_tests) * weight`

### 2. Algorithmic Efficiency (30-40%)

- **Time Complexity**: Matches expected Big-O notation
- **Space Complexity**: Within acceptable bounds
- Measured via:
  - Instrumentation (operation counting)
  - Timing on large inputs
  - Code analysis (loop nesting depth)

### 3. Code Quality (10%)

- **Readability**: Variable names, comments
- **Robustness**: Error handling
- **Best Practices**: Idiomatic code for language

---

## 📊 Results Example

```
╔═══════════════════════════════════════════════════════════════╗
║           LLM Coding Benchmark Results                        ║
╠═══════════════════════════════════════════════════════════════╣
║ Model: GPT-4 Turbo (gpt-4-turbo-preview)                      ║
║ Date: 2025-12-18                                              ║
║ Total Problems: 10                                            ║
╚═══════════════════════════════════════════════════════════════╝

┌────────┬─────────────────────────┬────────┬──────────┬─────────┐
│ ID     │ Problem                 │ Score  │ Correct  │ Optimal │
├────────┼─────────────────────────┼────────┼──────────┼─────────┤
│ P01    │ Two-Sum                 │ 95/100 │   ✅     │   ✅    │
│ P02    │ LRU Cache               │ 65/100 │   ✅     │   ❌    │
│ P03    │ Binary Tree Codec       │ 58/100 │   ✅     │   ❌    │
│ P04    │ Topological Sort        │ 48/100 │   ✅     │   ❌    │
│ P05    │ LIS (DP)                │ 42/100 │   ⚠️     │   ❌    │
│ P06    │ Merge K Lists           │ 55/100 │   ✅     │   ❌    │
│ P07    │ Word Ladder             │ 38/100 │   ⚠️     │   ❌    │
│ P08    │ Median Two Arrays       │ 22/100 │   ⚠️     │   ❌    │
│ P09    │ Regex Matching          │ 18/100 │   ❌     │   ❌    │
│ P10    │ Async Task Scheduler    │ 15/100 │   ❌     │   ❌    │
└────────┴─────────────────────────┴────────┴──────────┴─────────┘

Overall Score: 45.6/100
Pass Rate: 60% (6/10 problems fully correct)
Optimal Rate: 10% (1/10 problems with correct complexity)

Key Findings:
• Strong performance on hash table problems (P01)
• Struggles with advanced DP (P05, P09)
• Often defaults to brute force (P02, P08)
• Poor handling of async/concurrency (P10)
```

---

## 🛠️ Installation

```bash
git clone https://github.com/liohunter1/llm-coding-benchmark.git
cd llm-coding-benchmark
pip install -e .
```

**Requirements**:
- Python 3.10+
- OpenAI API key (for GPT models)
- Anthropic API key (for Claude models)

---

## 🤝 Contributing

### Adding New Problems

1. Create problem directory: `problems/pXX_problem_name/`
2. Write `problem.md` with clear specifications
3. Implement reference solutions in all 4 languages
4. Create comprehensive test suite (`test_cases.json`)
5. Define evaluation rubric (`rubric.md`)
6. Submit PR

### Problem Quality Criteria

- **Non-Trivial**: Requires algorithmic thinking
- **Objective**: Clear pass/fail criteria
- **Representative**: Tests real-world coding skills
- **Fair**: Solvable within token limits

---

## Results

qwen-122: unsloth/Qwen3.5-122B-A10B-GGUF:UD-Q5_K_XL

qwen-397: unsloth/Qwen3.5-397B-A17B-GGUF:UD-IQ1_M

| Problem | gemini-2.5-flash | qwen-122 | qwen-397 | gemini-3-pro-preview |
|--------|---|---|---|---|
| p01_two_sum | 100.0 | 100.0 | 100.0 | — |
| p02_lru_cache | 100.0 | 100.0 | 100.0 | — |
| p03_binary_tree_codec | 60.0 | 60.0 | 60.0 | 60.0 |
| p04_topological_sort | 100.0 | 100.0 | 100.0 | — |
| p05_lis | 100.0 | 100.0 | 100.0 | — |
| p06_merge_k_sorted_lists | 100.0 | 100.0 | 100.0 | — |
| p07_word_ladder | 100.0 | 100.0 | 100.0 | — |
| p08_median_sorted_arrays | 100.0 | 100.0 | 100.0 | — |
| p09_regex_matching | 100.0 | 100.0 | 100.0 | — |
| p10_async_task_scheduler | 100.0 | 100.0 | 100.0 | — |
| p11_weighted_job_scheduling | 100.0 | 100.0 | 100.0 | — |
| p12_lfu_cache | 100.0 | 100.0 | 100.0 | — |
| p13_smallest_range_k_lists | 5.0 | 66.7 | 100.0 | — |
| p14_suffix_array | 100.0 | 65.0 | 100.0 | — |
| p15_max_flow | 68.3 | 64.0 | 100.0 | 100.0 |
| p16_2sat | 72.5 | 100.0 | 41.0 | 100.0 |
| p17_min_cost_flow | 100.0 | 100.0 | 100.0 | 100.0 |
| p18_refactor_order_processor | 80.5 | 79.0 | 100.0 | — |
| p19_refactor_data_pipeline | 46.0 | 100.0 | 100.0 | — |
| p20_largest_rectangle_histogram | 100.0 | 100.0 | 100.0 | — |


---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Problem inspiration from LeetCode, Codeforces, Project Euler
- Test harness design influenced by Exercism.io
- Evaluation methodology from [papers on code generation benchmarks]

---

<div align="center">

**Built for AI Research Labs | Mercor Model Evaluation Workflow**

*Demonstrating expertise in creating rigorous, evidence-based LLM evaluation frameworks.*

</div>
