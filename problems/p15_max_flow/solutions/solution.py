"""
Reference solution for Maximum Network Flow using Dinic's Algorithm.

Time Complexity: O(V^2 * E)
Space Complexity: O(V + E)

Dinic's algorithm alternates between:
  1. BFS to build a level graph (shortest-path layering from source)
  2. DFS to push blocking flows through the level graph

The "current arc" optimization skips edges already fully explored in the
DFS phase, which is critical for achieving the O(V^2 E) bound.

Edges are stored in a flat list where edge i and edge i^1 are forward/reverse
pairs. This allows O(1) access to the reverse edge for residual updates.
"""

from collections import deque


def max_flow(n: int, edges: list[list[int]], source: int, sink: int) -> int:
    graph: list[list[int]] = [[] for _ in range(n)]
    edge_list: list[list[int]] = []

    def add_edge(u: int, v: int, cap: int) -> None:
        graph[u].append(len(edge_list))
        edge_list.append([v, cap])
        graph[v].append(len(edge_list))
        edge_list.append([u, 0])

    for u, v, cap in edges:
        add_edge(u, v, cap)

    def bfs() -> bool:
        """Build level graph via BFS. Returns True if sink is reachable."""
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

    def dfs(u: int, pushed: int) -> int:
        """Find blocking flow via DFS with current arc optimization."""
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
            f = dfs(source, float("inf"))
            if f == 0:
                break
            total += f

    return total


if __name__ == "__main__":
    assert max_flow(4, [[0, 1, 10], [0, 2, 10], [1, 2, 2], [1, 3, 4], [2, 3, 8]], 0, 3) == 12
    assert max_flow(6, [
        [0, 1, 16], [0, 2, 13], [1, 2, 10], [1, 3, 12],
        [2, 1, 4], [2, 4, 14], [3, 2, 9], [3, 5, 20],
        [4, 3, 7], [4, 5, 4]
    ], 0, 5) == 23
    assert max_flow(2, [[0, 1, 100]], 0, 1) == 100
    assert max_flow(4, [[0, 1, 1000000], [0, 2, 1000000], [1, 3, 1000000], [2, 3, 1000000]], 0, 3) == 2000000
    assert max_flow(3, [[0, 1, 5], [0, 1, 3]], 0, 1) == 8
    assert max_flow(3, [], 0, 2) == 0
    print("All tests passed!")
