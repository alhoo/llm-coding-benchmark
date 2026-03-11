# Problem P16: 2-SAT Solver (Kosaraju's / Tarjan's SCC)

## Problem Statement

Given a boolean formula in **2-CNF** (conjunctive normal form where each clause has exactly 2 literals), determine whether the formula is **satisfiable**. If it is, return a satisfying assignment; otherwise, return `None`.

The formula has `n` boolean variables numbered `1` to `n`. Each clause is a disjunction of two literals, where a literal is either a variable `x_i` (represented as positive integer `i`) or its negation `¬x_i` (represented as negative integer `-i`).

Implement the function `solve_2sat(n, clauses)` that returns a list of `n` booleans representing a satisfying assignment, or `None` if unsatisfiable.

Your implementation must run in **O(n + m)** time where `m` is the number of clauses, using **Strongly Connected Components** (Kosaraju's or Tarjan's algorithm) on the implication graph.

---

## Examples

### Example 1:
```
Input:
  n = 3
  clauses = [[1, 2], [-1, 3], [-2, -3]]

Output: [True, True, True]  (or any valid assignment)

Explanation:
  Formula: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)
  Assignment x1=T, x2=T, x3=T:
    (T ∨ T) = T  ✓
    (F ∨ T) = T  ✓
    (F ∨ F) = F  ✗
  Assignment x1=T, x2=F, x3=T:
    (T ∨ F) = T  ✓
    (F ∨ T) = T  ✓
    (T ∨ F) = T  ✓  → SAT
```

### Example 2:
```
Input:
  n = 1
  clauses = [[1, 1], [-1, -1]]

Output: None

Explanation:
  Formula: (x1 ∨ x1) ∧ (¬x1 ∨ ¬x1) = x1 ∧ ¬x1
  No assignment satisfies this. → UNSAT
```

### Example 3:
```
Input:
  n = 2
  clauses = [[1, -2], [-1, 2]]

Output: [True, True]  (or [False, False])

Explanation:
  Formula: (x1 ∨ ¬x2) ∧ (¬x1 ∨ x2) = (x1 ↔ x2)
  Any assignment where x1 = x2 works.
```

### Example 4:
```
Input:
  n = 4
  clauses = [[1, 2], [-1, -2], [3, 4], [-3, -4], [1, 3], [-2, -4]]

Output: [True, False, True, False]  (or any valid assignment)

Explanation:
  Clauses 1-2 force x1 XOR x2. Clauses 3-4 force x3 XOR x4.
  Clause 5 requires x1 or x3. Clause 6 requires ¬x2 or ¬x4.
  x1=T, x2=F, x3=T, x4=F satisfies all clauses.
```

### Example 5:
```
Input:
  n = 2
  clauses = [[1, 2], [1, -2], [-1, 2], [-1, -2]]

Output: None

Explanation:
  Formula: (x1 ∨ x2) ∧ (x1 ∨ ¬x2) ∧ (¬x1 ∨ x2) ∧ (¬x1 ∨ ¬x2)
  First two clauses force x1. Last two clauses force ¬x1. → UNSAT
```

---

## Constraints

- `1 <= n <= 100,000`
- `0 <= len(clauses) <= 200,000`
- Each clause is `[a, b]` where `a` and `b` are non-zero integers with `1 <= |a|, |b| <= n`
- A positive literal `i` means variable `x_i` is true
- A negative literal `-i` means variable `x_i` is false
- Clauses may be duplicated
- A clause may contain the same variable twice (e.g., `[x, x]` which forces `x` to be true)
- Tautological clauses like `[x, -x]` are always satisfied and may appear

---

## Hints

1. **Implication Graph**: For each clause `(a ∨ b)`, add two directed edges to the implication graph: `¬a → b` and `¬b → a`. This encodes the logical equivalence: if `a` is false, then `b` must be true (and vice versa).

2. **Variable Encoding**: Map variable `x_i` to node `2(i-1)` (true literal) and node `2(i-1)+1` (false literal). The negation of node `u` is `u ^ 1` (XOR with 1).

3. **SCC Decomposition**: Use Kosaraju's algorithm (two-pass DFS) or Tarjan's algorithm to find all strongly connected components.
   - **Unsatisfiable** if and only if some variable `x_i` and `¬x_i` are in the same SCC.
   - **Assignment**: For each variable, set it to `True` if its true-literal's SCC comes **later** in topological order than its false-literal's SCC.

4. **Iterative DFS**: Python's default recursion limit (~1000) is too low for large inputs. Use an iterative DFS implementation to avoid `RecursionError`.

5. **Kosaraju's Algorithm**:
   - Phase 1: Iterative DFS on the original implication graph, recording nodes in finish order.
   - Phase 2: Process nodes in reverse finish order, running DFS/BFS on the **reverse** graph to identify SCCs.
   - SCCs found in Phase 2 are naturally in topological order.

---

## Function Signature

### Python
```python
def solve_2sat(n: int, clauses: list[list[int]]) -> list[bool] | None:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — Returns a valid satisfying assignment for SAT instances, `None` for UNSAT instances
2. **Time Complexity** (35 points) — O(n + m) using SCC-based approach (not brute-force or backtracking)
3. **Code Quality** (15 points) — Clean implication graph construction, proper SCC decomposition, correct assignment extraction
