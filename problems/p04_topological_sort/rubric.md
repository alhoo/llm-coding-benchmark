# Evaluation Rubric: P04 - Topological Sort

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Basic DAG | 10 | Simple directed acyclic graph |
| Multiple valid orderings | 10 | Any valid topological order accepted |
| Disconnected graph | 10 | Isolated nodes included in output |
| Single node | 5 | One node, no edges |
| Chain graph | 10 | Linear: 0→1→2→3→4 |
| Dense graph | 5 | Many edges, still a DAG |

**Validation**: Output is valid if for every edge `u→v`, `u` appears before `v`.

---

## 2. Cycle Detection (30 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Simple cycle (A→B→A) | 10 | Two-node cycle |
| Self-loop | 10 | Node with edge to itself |
| Longer cycle | 10 | Cycle of length 4+ |

**Scoring**: Returns `[]` for all cycle cases = 30 points. Misses any = 0 points.

---

## 3. Time Complexity (10 points)

| Implementation | Points |
|----------------|--------|
| O(V + E) — Kahn's or DFS | 10 |
| O(V² + E) or worse | 0 |

---

## 4. Code Quality (10 points)

- ✅ **10 points**: Clean implementation of Kahn's algorithm or DFS, clear variable naming
- ⚠️ **5 points**: Correct but hard to follow
- ❌ **0 points**: Spaghetti code

---

## Common LLM Failures

### ❌ Failure Pattern 1: Cycle Detection Missing

```python
def topological_sort(n, edges):
    # Builds correct order for DAGs but never checks for cycles
    # Returns partial order when cycle exists instead of []
```

**Score**: 50/100

---

### ❌ Failure Pattern 2: Kahn's — Wrong Cycle Check

```python
# Correct: check if len(result) == n after BFS
# Wrong: check if queue is empty (queue can be empty before all nodes are processed)
if not queue:
    return result  # ❌ May return partial result instead of []
```

---

## ✅ Reference Solution (Kahn's Algorithm)

```python
from collections import deque

def topological_sort(n: int, edges: list[list[int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque(i for i in range(n) if in_degree[i] == 0)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []
```

**Score**: 100/100
