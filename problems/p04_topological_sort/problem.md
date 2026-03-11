# Problem P04: Topological Sort

## Problem Statement

Given a directed acyclic graph (DAG) with `n` nodes labeled from `0` to `n-1`, and a list of directed edges, return a **topological ordering** of the nodes.

A topological ordering is an ordering of nodes such that for every directed edge `u → v`, node `u` comes before node `v` in the ordering.

If the graph contains a **cycle**, return an empty list `[]`.

---

## Examples

### Example 1:
```
Input: n = 6, edges = [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]
Output: [5, 4, 2, 3, 1, 0]  (one valid ordering)

Explanation:
  5 → 2 → 3 → 1
  5 → 0
  4 → 0
  4 → 1
```

### Example 2:
```
Input: n = 2, edges = [[0,1],[1,0]]
Output: []  (cycle detected)
```

### Example 3:
```
Input: n = 1, edges = []
Output: [0]
```

---

## Constraints

- `1 <= n <= 2000`
- `0 <= edges.length <= 5000`
- `edges[i].length == 2`
- `0 <= edges[i][0], edges[i][1] < n`
- All edges are unique.

---

## Hints

1. **Kahn's Algorithm**: Use in-degree counting and a queue (BFS approach).
2. **DFS approach**: Use DFS with visited/in-progress state to detect cycles, then reverse the finish order.
3. A cycle exists if not all nodes are included in the topological order.

---

## Function Signature

### Python
```python
def topological_sort(n: int, edges: list[list[int]]) -> list[int]:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — Returns valid topological ordering
2. **Cycle Detection** (30 points) — Returns `[]` when graph has a cycle
3. **Time Complexity** (10 points) — O(V + E)
4. **Code Quality** (10 points) — Clear, idiomatic implementation
