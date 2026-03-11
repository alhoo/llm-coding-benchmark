# Problem P17: Minimum Cost Maximum Flow (Successive Shortest Paths + SPFA)

## Problem Statement

Given a directed graph with `n` nodes (numbered `0` to `n-1`), a list of directed edges each with an integer **capacity** and an integer **cost per unit of flow**, a source node `s`, and a sink node `t`, compute the **maximum flow** from `s` to `t` and the **minimum total cost** to achieve that maximum flow.

Implement the function `min_cost_max_flow(n, edges, source, sink)` that returns a tuple `(max_flow, min_cost)`.

Your implementation must use the **Successive Shortest Paths** algorithm with **SPFA** (Shortest Path Faster Algorithm, a queue-based Bellman-Ford variant) for finding minimum-cost augmenting paths, achieving a time complexity of **O(V · E · F)** where F is the max flow value.

---

## Examples

### Example 1:
```
Input:
  n = 2
  edges = [[0, 1, 5, 3]]
  source = 0, sink = 1

Output: (5, 15)

Explanation:
  Single edge with capacity 5 and cost 3 per unit.
  Push 5 units at cost 3 each → total cost = 15.
```

### Example 2:
```
Input:
  n = 4
  edges = [[0, 1, 5, 1], [1, 3, 5, 2], [0, 2, 5, 10], [2, 3, 5, 20]]
  source = 0, sink = 3

Output: (10, 165)

Explanation:
  Path A: 0→1→3, capacity 5, cost per unit = 1+2 = 3
  Path B: 0→2→3, capacity 5, cost per unit = 10+20 = 30
  Cheapest path (A) is used first: 5 units × cost 3 = 15
  Then path B: 5 units × cost 30 = 150
  Total: flow = 10, cost = 15 + 150 = 165
```

### Example 3:
```
Input:
  n = 4
  edges = [[0, 1, 3, 1], [0, 2, 2, 5], [1, 3, 2, 3], [2, 3, 3, 2], [1, 2, 3, 1]]
  source = 0, sink = 3

Output: (5, 26)

Explanation:
  Cheapest path: 0→1→3, cost 1+3=4, or 0→1→2→3, cost 1+1+2=4 (tied).
  The SPFA finds minimum-cost augmenting paths and reroutes flow through
  the residual graph (including negative-cost reverse edges) as needed.
  After all augmenting paths: flow = 5, cost = 26.
```

### Example 4:
```
Input:
  n = 5
  edges = [[0, 1, 10, 2], [0, 2, 10, 8], [1, 3, 7, 5], [2, 3, 7, 1],
           [1, 2, 5, 3], [3, 4, 15, 4]]
  source = 0, sink = 4

Output: (14, 159)

Explanation:
  Multiple augmenting paths with different costs. The algorithm finds
  cheapest augmenting paths first, re-routing flow through the residual
  graph as needed to minimize total cost.
```

### Example 5:
```
Input:
  n = 3
  edges = [[0, 1, 5, 1], [0, 1, 5, 3]]
  source = 0, sink = 1

Output: (10, 20)

Explanation:
  Parallel edges: one with cost 1, one with cost 3.
  Cheaper edge used first: 5 units × 1 = 5.
  Then expensive edge: 5 units × 3 = 15.
  Total: flow = 10, cost = 5 + 15 = 20.
```

---

## Constraints

- `2 <= n <= 300`
- `0 <= len(edges) <= 5,000`
- Each edge is `[u, v, capacity, cost]` where:
  - `0 <= u, v < n`
  - `1 <= capacity <= 10,000`
  - `0 <= cost <= 1,000`
- `0 <= source, sink < n` and `source != sink`
- There may be **parallel edges** (multiple edges between the same pair of nodes)
- There may be **anti-parallel edges** (edges in both directions between two nodes)
- The graph may be disconnected (in which case max flow is 0 and cost is 0)
- All edge costs are non-negative in the input (but the residual graph will have negative-cost reverse edges)

---

## Hints

1. **Residual Graph with Costs**: Build a residual graph where each edge `(u, v, cap, cost)` has a reverse edge `(v, u, 0, -cost)`. When flow is pushed through an edge, decrease its residual capacity and increase the reverse edge's capacity. The reverse edge's negative cost allows "undoing" flow to find cheaper alternatives.

2. **SPFA (Bellman-Ford with Queue)**: Because the residual graph has negative-cost edges (from reverse edges), Dijkstra's algorithm cannot be used directly. Use SPFA — a queue-based relaxation algorithm that handles negative edges:
   - Maintain a distance array initialized to infinity (0 for source).
   - Use a deque/queue. When a shorter path to a node is found, add it to the queue if not already present.
   - Track the predecessor edge for each node to reconstruct the augmenting path.

3. **Edge Representation**: Store edges in a flat list where edge `i` and edge `i ^ 1` are forward/reverse pairs (same as Dinic's algorithm from P15). Each edge stores `[destination, capacity, cost]`.

4. **Successive Shortest Paths**: Repeatedly:
   - Find the shortest (minimum cost) augmenting path from source to sink using SPFA.
   - Determine the bottleneck capacity along this path.
   - Push flow along the path, updating residual capacities.
   - Accumulate `flow × path_cost` into total cost.
   - Stop when no augmenting path exists.

5. **Path Reconstruction**: After SPFA, trace back from sink to source using the predecessor edge array. The predecessor of node `v` gives the edge used to reach `v`. The source of that edge is `edge_list[eid ^ 1][0]` (the destination of the reverse edge).

---

## Function Signature

### Python
```python
def min_cost_max_flow(n: int, edges: list[list[int]], source: int, sink: int) -> tuple[int, int]:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return the correct (max_flow, min_cost) tuple
2. **Time Complexity** (35 points) — O(V · E · F) via Successive Shortest Paths with SPFA
3. **Code Quality** (15 points) — Clean residual graph with costs, proper SPFA, correct path reconstruction
