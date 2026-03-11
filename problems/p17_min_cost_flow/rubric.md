# Evaluation Rubric: P17 - Minimum Cost Maximum Flow (Successive Shortest Paths + SPFA)

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Single edge | 5 | Basic flow = capacity, cost = capacity × unit_cost |
| Two paths different costs | 10 | Cheaper path used first, correct total cost |
| Parallel edges | 5 | Multiple edges between same pair sum correctly |
| Anti-parallel edges | 5 | Edges in both directions handled properly |
| Disconnected sink | 5 | Returns (0, 0) when no path exists |
| Diamond rerouting | 10 | Residual graph rerouting produces optimal cost |
| Complex network | 10 | 6+ node network with multiple cost tradeoffs |

**Scoring**:
- Pass all: 50 points
- Fail 1-2 cases: 35 points
- Fail 3-4 cases: 20 points
- Fail 5+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Expected: O(V · E · F) via Successive Shortest Paths + SPFA

| Implementation | Points | Description |
|----------------|--------|-------------|
| SPFA-based successive shortest paths | 35 | Correct and efficient |
| Bellman-Ford (non-SPFA) successive shortest paths | 30 | Correct, slightly slower in practice |
| Dijkstra with Johnson's potentials | 35 | Alternative correct approach |
| Naive Ford-Fulkerson + separate cost tracking | 10 | May give wrong costs on complex graphs |
| Brute force / incorrect | 0 | Unacceptable |

**Verification Method**:
- Timing test: 200 nodes, 2000 edges should complete in < 10 seconds
- Dense graph test: 100 nodes, ~700 edges should complete in < 10 seconds

---

## 3. Code Quality (15 points)

### Residual Graph with Costs (6 points)
- ✅ **6 points**: Clean edge-pair representation (i ↔ i^1), reverse edges have negative cost
- ⚠️ **3 points**: Works but uses separate data structures for forward/reverse tracking
- ❌ **0 points**: No reverse edges with costs, or costs not negated on reverse edges

### SPFA / Shortest Path (5 points)
- ✅ **5 points**: Proper SPFA with queue, handles negative costs from reverse edges
- ⚠️ **3 points**: Uses Dijkstra (fails with negative-cost reverse edges) or non-optimal shortest path
- ❌ **0 points**: No shortest path — uses arbitrary augmenting path (wrong costs)

### Path Reconstruction (4 points)
- ✅ **4 points**: Correct bottleneck finding and flow pushing along predecessor chain
- ⚠️ **2 points**: Works but inefficient (e.g., re-runs BFS to find path)
- ❌ **0 points**: Wrong path reconstruction — flow tracking breaks

---

## Common LLM Failures

### ❌ Failure Pattern 1: Reverse Edges Missing Negative Cost

```python
def add_edge(u, v, cap, cost):
    edge_list.append([v, cap, cost])
    edge_list.append([u, 0, 0])  # ❌ Should be -cost, not 0
```

**Score**: 20/100 (Flow is correct but cost is wrong — can't "undo" costly flow decisions)

---

### ❌ Failure Pattern 2: Using Dijkstra Instead of SPFA

```python
# ❌ Dijkstra cannot handle negative-weight edges from reverse edges
import heapq
while pq:
    d, u = heapq.heappop(pq)
    # Negative-cost reverse edges are never relaxed correctly
```

**Score**: 40/100 (Works on some inputs where no rerouting is needed, fails on complex cases)

Note: Dijkstra with Johnson's potentials (initial Bellman-Ford + reduced costs) IS correct but must be implemented carefully.

---

### ❌ Failure Pattern 3: Wrong Path Reconstruction

```python
# ❌ Tracking predecessor by node instead of edge
prev_node[v] = u
# Later: can't identify WHICH edge was used (problem with parallel edges)
```

**Score**: 30/100 (Breaks on parallel edges — updates wrong edge's capacity)

---

### ❌ Failure Pattern 4: Cost Accumulated Wrong

```python
# ❌ Adds cost per edge instead of (flow × total_path_cost)
total_cost += edge_cost  # Should be: total_cost += flow * dist[sink]
```

**Score**: 25/100 (Cost is always wrong)

---

### ❌ Failure Pattern 5: Not Maximizing Flow

```python
# ❌ Stops after finding one augmenting path instead of all
path = spfa(source, sink)
if path:
    push_flow(path)
    return (flow, cost)  # Should keep looping until no path exists
```

**Score**: 20/100 (Returns suboptimal flow for most inputs)

---

### ❌ Failure Pattern 6: Parallel Edges Overwritten

```python
capacity = {}
cost_map = {}
for u, v, cap, c in edges:
    capacity[(u, v)] = cap   # ❌ Overwrites previous parallel edge
    cost_map[(u, v)] = c
```

**Score**: 25/100 (Wrong answer when parallel edges exist)

---

## ✅ Reference Solution

```python
from collections import deque

def min_cost_max_flow(n, edges, source, sink):
    graph = [[] for _ in range(n)]
    edge_list = []

    def add_edge(u, v, cap, cost):
        graph[u].append(len(edge_list))
        edge_list.append([v, cap, cost])
        graph[v].append(len(edge_list))
        edge_list.append([u, 0, -cost])

    for u, v, cap, cost in edges:
        add_edge(u, v, cap, cost)

    total_flow = 0
    total_cost = 0
    INF = float('inf')

    while True:
        dist = [INF] * n
        dist[source] = 0
        in_queue = [False] * n
        prev_edge = [-1] * n

        q = deque([source])
        in_queue[source] = True

        while q:
            u = q.popleft()
            in_queue[u] = False
            for eid in graph[u]:
                v, cap, cost = edge_list[eid]
                if cap > 0 and dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    prev_edge[v] = eid
                    if not in_queue[v]:
                        q.append(v)
                        in_queue[v] = True

        if dist[sink] == INF:
            break

        flow = INF
        v = sink
        while v != source:
            eid = prev_edge[v]
            flow = min(flow, edge_list[eid][1])
            v = edge_list[eid ^ 1][0]

        v = sink
        while v != source:
            eid = prev_edge[v]
            edge_list[eid][1] -= flow
            edge_list[eid ^ 1][1] += flow
            v = edge_list[eid ^ 1][0]

        total_flow += flow
        total_cost += flow * dist[sink]

    return total_flow, total_cost
```

**Score**: 100/100
- ✅ Correctness: Handles parallel, anti-parallel, rerouting, zero-cost, disconnected
- ✅ Time Complexity: O(V · E · F) with SPFA
- ✅ Code Quality: Clean edge pairs, proper SPFA, correct cost accumulation
