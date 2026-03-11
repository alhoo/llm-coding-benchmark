"""
Reference solution for Minimum Cost Maximum Flow using Successive Shortest Paths.

Time Complexity: O(V * E * F) where F is the max flow value
Space Complexity: O(V + E)

Algorithm:
  1. Build a residual graph where each edge (u, v, cap, cost) has a reverse edge
     (v, u, 0, -cost). Edges are stored in a flat list; edge i and i^1 are pairs.
  2. Repeatedly find the shortest (cheapest) augmenting path from source to sink
     using SPFA (Bellman-Ford with queue), which handles negative-cost reverse edges.
  3. Push the maximum possible flow along the cheapest path.
  4. Accumulate flow * path_cost into total cost.
  5. Stop when no augmenting path exists.
"""

from collections import deque


def min_cost_max_flow(
    n: int, edges: list[list[int]], source: int, sink: int
) -> tuple[int, int]:
    graph: list[list[int]] = [[] for _ in range(n)]
    edge_list: list[list[int]] = []

    def add_edge(u: int, v: int, cap: int, cost: int) -> None:
        graph[u].append(len(edge_list))
        edge_list.append([v, cap, cost])
        graph[v].append(len(edge_list))
        edge_list.append([u, 0, -cost])

    for u, v, cap, cost in edges:
        add_edge(u, v, cap, cost)

    total_flow = 0
    total_cost = 0
    INF = float("inf")

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

        # Find bottleneck capacity along shortest path
        flow = INF
        v = sink
        while v != source:
            eid = prev_edge[v]
            flow = min(flow, edge_list[eid][1])
            v = edge_list[eid ^ 1][0]

        # Push flow along the path
        v = sink
        while v != source:
            eid = prev_edge[v]
            edge_list[eid][1] -= flow
            edge_list[eid ^ 1][1] += flow
            v = edge_list[eid ^ 1][0]

        total_flow += flow
        total_cost += flow * dist[sink]

    return total_flow, total_cost


if __name__ == "__main__":
    assert min_cost_max_flow(2, [[0, 1, 5, 3]], 0, 1) == (5, 15)

    assert min_cost_max_flow(4, [
        [0, 1, 5, 1], [1, 3, 5, 2], [0, 2, 5, 10], [2, 3, 5, 20]
    ], 0, 3) == (10, 165)

    assert min_cost_max_flow(3, [[0, 1, 5, 1], [0, 1, 5, 3]], 0, 1) == (10, 20)

    assert min_cost_max_flow(3, [], 0, 2) == (0, 0)

    print("All tests passed!")
