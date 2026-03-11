# Evaluation Rubric: P15 - Maximum Network Flow (Dinic's Algorithm)

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Simple diamond | 5 | 4-node graph, single bottleneck |
| CLRS example | 10 | Classic 6-node textbook example |
| Parallel edges | 10 | Multiple edges between same pair — must sum capacities |
| Anti-parallel edges | 5 | Edges in both directions between two nodes |
| Disconnected sink | 5 | Sink unreachable → flow = 0 |
| Bottleneck chain | 5 | Linear chain with a single bottleneck |
| Unit capacity | 5 | All capacities = 1, tests max flow through unit network |
| Complex network | 5 | 7-node graph with multiple augmenting paths |

**Scoring**:
- Pass all: 50 points
- Fail 1-2 cases: 35 points
- Fail 3-4 cases: 20 points
- Fail 5+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Expected: O(V²E) via Dinic's Algorithm

| Implementation | Points | Description |
|----------------|--------|-------------|
| Dinic's with current arc optimization | 35 | Optimal O(V²E) |
| Dinic's without current arc optimization | 25 | Correct but slower in practice |
| Edmonds-Karp (BFS-based Ford-Fulkerson) | 20 | O(VE²) — suboptimal |
| Ford-Fulkerson with DFS | 10 | O(E × max_flow) — not polynomial in capacity |
| Brute force / incorrect | 0 | Unacceptable |

**Verification Method**:
- Timing test: 500 nodes, 5000 edges should complete in < 5 seconds
- Check for BFS level graph + DFS blocking flow structure

---

## 3. Code Quality (15 points)

### Residual Graph Design (6 points)
- ✅ **6 points**: Clean edge-pair representation (i ↔ i^1), proper reverse edge management
- ⚠️ **3 points**: Works but uses separate forward/reverse edge tracking with dicts
- ❌ **0 points**: No proper residual graph — only decrements forward edges

### BFS/DFS Separation (5 points)
- ✅ **5 points**: Clear BFS for level graph, separate DFS for blocking flow
- ⚠️ **3 points**: Combined BFS+DFS or unclear separation
- ❌ **0 points**: No level graph, just repeated DFS/BFS

### Edge Cases (4 points)
- ✅ **4 points**: Handles parallel edges, anti-parallel edges, disconnected graphs, self-loops
- ❌ **0 points**: Crashes or wrong answer on edge cases

---

## Common LLM Failures

### ❌ Failure Pattern 1: No Reverse Edges in Residual Graph

```python
def max_flow(n, edges, source, sink):
    graph = defaultdict(list)
    for u, v, cap in edges:
        graph[u].append((v, cap))
    # ❌ No reverse edges — cannot "undo" flow decisions
    # Result: suboptimal flow, wrong answer
```

**Score**: 15/100 (Fundamentally broken — cannot find augmenting paths correctly)

---

### ❌ Failure Pattern 2: Ford-Fulkerson with DFS (Not Dinic's)

```python
def max_flow(n, edges, source, sink):
    while True:
        # ❌ Simple DFS to find any augmenting path
        path = dfs_find_path(source, sink)
        if not path:
            break
        # Push flow along path
```

**Score**: 55/100 (Correct for small inputs but O(E × max_flow) — exponential in capacity)

---

### ❌ Failure Pattern 3: Missing Current Arc Optimization

```python
def dfs(u, pushed):
    for eid in graph[u]:  # ❌ Always iterates from the first edge
        v, cap = edge_list[eid]
        if cap > 0 and level[v] == level[u] + 1:
            d = dfs(v, min(pushed, cap))
            if d > 0:
                # update edges
                return d
    return 0
```

**Score**: 75/100 (Correct but O(VE²) in worst case — significantly slower)

---

### ❌ Failure Pattern 4: Parallel Edges Not Handled

```python
def max_flow(n, edges, source, sink):
    cap = {}
    for u, v, c in edges:
        cap[(u, v)] = c  # ❌ Overwrites if (u,v) appears multiple times
```

**Score**: 40/100 (Wrong answer when parallel edges exist)

---

### ❌ Failure Pattern 5: Reverse Edge Index Wrong

```python
# Forward edge at index i, reverse should be at i^1
# But edges are not added in pairs!
def add_edge(u, v, cap):
    graph[u].append(len(edge_list))
    edge_list.append([v, cap])
    # ❌ Forgot to add reverse edge immediately after
    # Later: edge_list[eid ^ 1] points to wrong edge
```

**Score**: 10/100 (Corrupted residual graph — flow tracking is completely wrong)

---

## ✅ Reference Solution

```python
from collections import deque

def max_flow(n, edges, source, sink):
    graph = [[] for _ in range(n)]
    edge_list = []

    def add_edge(u, v, cap):
        graph[u].append(len(edge_list))
        edge_list.append([v, cap])
        graph[v].append(len(edge_list))
        edge_list.append([u, 0])

    for u, v, cap in edges:
        add_edge(u, v, cap)

    def bfs():
        level[:] = [-1] * n
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for eid in graph[u]:
                v, cap = edge_list[eid]
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[sink] != -1

    def dfs(u, pushed):
        if u == sink:
            return pushed
        while iter_ptr[u] < len(graph[u]):
            eid = graph[u][iter_ptr[u]]
            v, cap = edge_list[eid]
            if cap > 0 and level[v] == level[u] + 1:
                d = dfs(v, min(pushed, cap))
                if d > 0:
                    edge_list[eid][1] -= d
                    edge_list[eid ^ 1][1] += d
                    return d
            iter_ptr[u] += 1
        return 0

    level = [-1] * n
    total = 0
    while bfs():
        iter_ptr = [0] * n
        while True:
            f = dfs(source, float('inf'))
            if f == 0:
                break
            total += f
    return total
```

**Score**: 100/100
- ✅ Correctness: All test cases pass (parallel edges, anti-parallel, disconnected)
- ✅ Time Complexity: O(V²E) with current arc optimization
- ✅ Code Quality: Clean edge-pair design, proper BFS/DFS separation
