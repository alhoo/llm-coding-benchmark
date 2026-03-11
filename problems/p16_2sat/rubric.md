# Evaluation Rubric: P16 - 2-SAT Solver (Kosaraju's / Tarjan's SCC)

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Forced True/False | 5 | Single variable forced by clause `[x, x]` or `[-x, -x]` |
| Contradiction (UNSAT) | 10 | x ∧ ¬x detected as unsatisfiable |
| Biconditional / XOR | 10 | Equivalence and XOR constraints produce correct assignment |
| Chain implications | 10 | Long chains of implications propagated correctly |
| Multi-variable SAT | 10 | 10+ variable instances return valid satisfying assignments |
| UNSAT detection | 5 | Various UNSAT patterns correctly return None |

**Scoring**:
- Pass all: 50 points
- Fail 1-2 cases: 35 points
- Fail 3-4 cases: 20 points
- Fail 5+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Expected: O(n + m) via SCC (Kosaraju's or Tarjan's)

| Implementation | Points | Description |
|----------------|--------|-------------|
| SCC-based with iterative DFS | 35 | Optimal O(n + m), handles large inputs |
| SCC-based with recursive DFS | 25 | Correct but hits RecursionError on large inputs |
| Backtracking / DPLL | 10 | Exponential worst-case |
| Brute force (enumerate all assignments) | 0 | O(2^n) — unacceptable |

**Verification Method**:
- Timing test: 50,000 variables, 100,000 clauses should complete in < 5 seconds
- Chain of 100,000 implications should not cause RecursionError

---

## 3. Code Quality (15 points)

### Implication Graph Construction (5 points)
- ✅ **5 points**: Correct `¬a → b` and `¬b → a` edges with clean literal-to-node mapping
- ⚠️ **3 points**: Works but uses string/dict-based graph instead of array-based
- ❌ **0 points**: Missing one direction of implication or wrong literal mapping

### SCC Algorithm (5 points)
- ✅ **5 points**: Clean Kosaraju's (two-pass) or Tarjan's with proper iterative DFS
- ⚠️ **3 points**: Correct SCC but recursive (breaks on large inputs)
- ❌ **0 points**: No SCC — uses ad-hoc reachability or brute force

### Assignment Extraction (5 points)
- ✅ **5 points**: Correct use of topological order of SCCs to assign variables
- ⚠️ **2 points**: Uses SCC but assignment direction is inverted (fails on some inputs)
- ❌ **0 points**: Random assignment or hardcoded values

---

## Common LLM Failures

### ❌ Failure Pattern 1: Wrong Implication Direction

```python
# Clause (a OR b)
# ❌ WRONG: adds a→b instead of ¬a→b
graph[node_a].append(node_b)
graph[node_b].append(node_a)
```

**Score**: 10/100 (Fundamentally broken implication graph)

---

### ❌ Failure Pattern 2: Recursive DFS Hits RecursionError

```python
def dfs(u):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs(v)  # ❌ Stack overflow on n=100,000
    order.append(u)
```

**Score**: 60/100 (Correct for small inputs, crashes on large chains)

---

### ❌ Failure Pattern 3: Inverted Assignment

```python
# ❌ WRONG direction — sets variable to True when it should be False
result[i] = comp[2*i] < comp[2*i + 1]  # inverted for Kosaraju's
# or
result[i] = comp[2*i] > comp[2*i + 1]  # inverted for Tarjan's
```

**Score**: 35/100 (UNSAT detection works, but SAT assignments are wrong ~50% of the time)

---

### ❌ Failure Pattern 4: No Reverse Graph in Kosaraju's

```python
# Phase 2 runs DFS on the SAME graph instead of the reverse graph
# ❌ SCCs are wrong — components are not strongly connected
for start in reversed(order):
    dfs_on_original_graph(start)  # should be reverse graph
```

**Score**: 15/100 (Wrong SCCs → wrong UNSAT detection and wrong assignments)

---

### ❌ Failure Pattern 5: Literal-to-Node Mapping Off-by-One

```python
def lit_to_node(x):
    if x > 0:
        return 2 * x      # ❌ Should be 2*(x-1)
    return 2 * (-x) + 1   # ❌ Should be 2*(-x-1)+1
```

**Score**: 5/100 (Node indices are wrong, causing incorrect edges and crashes)

---

## ✅ Reference Solution

```python
from collections import deque

def solve_2sat(n, clauses):
    num_nodes = 2 * n
    adj = [[] for _ in range(num_nodes)]
    radj = [[] for _ in range(num_nodes)]

    def lit_to_node(x):
        if x > 0:
            return 2 * (x - 1)
        return 2 * (-x - 1) + 1

    for a, b in clauses:
        na, nb = lit_to_node(a), lit_to_node(b)
        adj[na ^ 1].append(nb)
        adj[nb ^ 1].append(na)
        radj[nb].append(na ^ 1)
        radj[na].append(nb ^ 1)

    # Kosaraju Phase 1: iterative DFS, record finish order
    order = []
    visited = [False] * num_nodes
    for start in range(num_nodes):
        if visited[start]:
            continue
        stack = [(start, 0)]
        visited[start] = True
        while stack:
            u, idx = stack[-1]
            if idx < len(adj[u]):
                stack[-1] = (u, idx + 1)
                v = adj[u][idx]
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(u)

    # Kosaraju Phase 2: BFS on reverse graph
    comp = [-1] * num_nodes
    comp_id = 0
    for start in reversed(order):
        if comp[start] != -1:
            continue
        queue = deque([start])
        comp[start] = comp_id
        while queue:
            u = queue.popleft()
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = comp_id
                    queue.append(v)
        comp_id += 1

    for i in range(n):
        if comp[2 * i] == comp[2 * i + 1]:
            return None

    return [comp[2 * i] > comp[2 * i + 1] for i in range(n)]
```

**Score**: 100/100
- ✅ Correctness: All SAT/UNSAT cases handled, valid assignments produced
- ✅ Time Complexity: O(n + m) with iterative Kosaraju's
- ✅ Code Quality: Clean literal mapping, proper two-phase SCC, correct assignment
