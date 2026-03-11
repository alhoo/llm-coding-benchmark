# Problem P15: Maximum Network Flow (Dinic's Algorithm)

## Problem Statement

Given a directed graph with `n` nodes (numbered `0` to `n-1`), a list of directed edges with integer capacities, a source node `s`, and a sink node `t`, compute the **maximum flow** from `s` to `t`.

Implement the function `max_flow(n, edges, source, sink)` that returns the maximum flow value.

Your implementation must use **Dinic's algorithm** (or an equivalent algorithm achieving **O(V² E)** time complexity).

---

## Examples

### Example 1:
```
Input:
  n = 4
  edges = [[0, 1, 10], [0, 2, 10], [1, 2, 2], [1, 3, 4], [2, 3, 8]]
  source = 0, sink = 3

Output: 12

Explanation:
  Flow paths:
    0 → 1 → 3: 4 units
    0 → 1 → 2 → 3: 2 units (using edge 1→2 capacity 2)
    0 → 2 → 3: 6 units
  Total flow: 4 + 2 + 6 = 12

  (0 → 1 sends 6, 0 → 2 sends 6; 1 → 3 sends 4, 1 → 2 sends 2, 2 → 3 sends 8)
```

### Example 2:
```
Input:
  n = 6
  edges = [[0, 1, 16], [0, 2, 13], [1, 2, 10], [1, 3, 12], [2, 1, 4], [2, 4, 14],
           [3, 2, 9], [3, 5, 20], [4, 3, 7], [4, 5, 4]]
  source = 0, sink = 5

Output: 23

Explanation:
  This is the classic CLRS max-flow example.
```

### Example 3:
```
Input:
  n = 2
  edges = [[0, 1, 100]]
  source = 0, sink = 1

Output: 100

Explanation: Single edge, flow equals edge capacity.
```

### Example 4:
```
Input:
  n = 4
  edges = [[0, 1, 1000000], [0, 2, 1000000], [1, 3, 1000000], [2, 3, 1000000]]
  source = 0, sink = 3

Output: 2000000

Explanation: Two parallel paths, each with capacity 1,000,000.
```

### Example 5:
```
Input:
  n = 3
  edges = [[0, 1, 5], [0, 1, 3]]
  source = 0, sink = 1

Output: 8

Explanation: Parallel edges between the same pair of nodes. Total capacity = 5 + 3 = 8.
```

---

## Constraints

- `2 <= n <= 500`
- `0 <= len(edges) <= 10,000`
- Each edge is `[u, v, capacity]` where `0 <= u, v < n` and `1 <= capacity <= 10^6`
- `0 <= source, sink < n` and `source != sink`
- There may be **parallel edges** (multiple edges between the same pair of nodes).
- There may be **anti-parallel edges** (edges in both directions between two nodes).
- The graph may be disconnected (in which case max flow is 0 if sink is unreachable).

---

## Hints

1. **Residual Graph**: Build a graph where each edge `(u, v, cap)` also has a reverse edge `(v, u, 0)`. When flow is pushed through an edge, decrease its residual capacity and increase the reverse edge's capacity.

2. **Dinic's Algorithm** has two phases per iteration:
   - **BFS phase**: Build a level graph from source. Assign levels to each node (distance from source in terms of edges with remaining capacity). If sink is unreachable, stop.
   - **DFS phase**: Find blocking flows using DFS on the level graph. Only traverse edges where `level[v] == level[u] + 1` and remaining capacity > 0.

3. **Current arc optimization**: For each node, remember which edge was last used in DFS to avoid re-scanning edges that cannot contribute more flow. This is critical for achieving O(V²E) complexity.

4. **Edge representation**: Store edges in a flat list. For edge at index `i`, its reverse edge is at index `i ^ 1` (XOR with 1). This works when edges are added in pairs (forward, reverse).

---

## Function Signature

### Python
```python
def max_flow(n: int, edges: list[list[int]], source: int, sink: int) -> int:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return the correct maximum flow value
2. **Time Complexity** (35 points) — O(V²E) via Dinic's algorithm (not Ford-Fulkerson with DFS or Edmonds-Karp alone)
3. **Code Quality** (15 points) — Clean residual graph construction, proper BFS/DFS separation, current arc optimization
