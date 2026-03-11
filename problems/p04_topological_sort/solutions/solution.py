"""
Reference solution for Topological Sort.
Uses Kahn's algorithm (BFS / in-degree approach).
Time Complexity: O(V + E)
Space Complexity: O(V + E)
"""

from collections import deque


def topological_sort(n: int, edges: list[list[int]]) -> list[int]:
    """
    Return a topological ordering of n nodes given directed edges.
    Returns [] if the graph contains a cycle.

    Args:
        n: Number of nodes (labeled 0 to n-1)
        edges: List of directed edges [u, v] meaning u → v

    Returns:
        A valid topological ordering, or [] if a cycle exists.
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    in_degree: list[int] = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue: deque[int] = deque(i for i in range(n) if in_degree[i] == 0)
    result: list[int] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []


def is_valid_topological_order(n: int, edges: list[list[int]], order: list[int]) -> bool:
    """Verify that the given order is a valid topological ordering."""
    if len(order) != n:
        return False
    position = {node: i for i, node in enumerate(order)}
    return all(position[u] < position[v] for u, v in edges)


if __name__ == "__main__":
    order = topological_sort(6, [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]])
    assert is_valid_topological_order(6, [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]], order)

    assert topological_sort(2, [[0, 1], [1, 0]]) == []

    assert topological_sort(1, []) == [0]

    print("All tests passed!")
