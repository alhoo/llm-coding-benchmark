"""
Reference solution for 2-SAT using Kosaraju's SCC algorithm.

Time Complexity: O(n + m) where n = variables, m = clauses
Space Complexity: O(n + m)

Approach:
  1. Build an implication graph: for clause (a ∨ b), add edges ¬a→b and ¬b→a.
  2. Find SCCs using Kosaraju's two-pass algorithm (iterative to avoid recursion limits).
  3. If any variable and its negation share an SCC, the formula is UNSAT.
  4. Otherwise, assign each variable based on topological order of its literal's SCC.

Variable encoding: literal x_i → node 2*(i-1), literal ¬x_i → node 2*(i-1)+1.
Negation: node u's negation is u ^ 1.
"""

from collections import deque


def solve_2sat(n: int, clauses: list[list[int]]) -> list[bool] | None:
    num_nodes = 2 * n
    adj: list[list[int]] = [[] for _ in range(num_nodes)]
    radj: list[list[int]] = [[] for _ in range(num_nodes)]

    def lit_to_node(x: int) -> int:
        if x > 0:
            return 2 * (x - 1)
        return 2 * (-x - 1) + 1

    for a, b in clauses:
        na, nb = lit_to_node(a), lit_to_node(b)
        adj[na ^ 1].append(nb)
        adj[nb ^ 1].append(na)
        radj[nb].append(na ^ 1)
        radj[na].append(nb ^ 1)

    # Kosaraju Phase 1: iterative DFS on adj, record finish order
    order: list[int] = []
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

    # Kosaraju Phase 2: BFS on radj in reverse finish order
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

    # In Kosaraju's, comp_id 0 is a source SCC (earliest in topological order).
    # A variable is True if its true-literal's SCC is later in topological order
    # (higher comp_id) than its false-literal's SCC.
    return [comp[2 * i] > comp[2 * i + 1] for i in range(n)]


if __name__ == "__main__":
    # SAT: (x1 ∨ x2) — many valid assignments
    result = solve_2sat(2, [[1, 2]])
    assert result is not None
    x1, x2 = result
    assert x1 or x2

    # UNSAT: x1 ∧ ¬x1
    assert solve_2sat(1, [[1, 1], [-1, -1]]) is None

    # SAT: x1 ↔ x2
    result = solve_2sat(2, [[1, -2], [-1, 2]])
    assert result is not None
    assert result[0] == result[1]

    # UNSAT: all four combinations
    assert solve_2sat(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]]) is None

    # SAT: no clauses
    result = solve_2sat(3, [])
    assert result is not None and len(result) == 3

    print("All tests passed!")
