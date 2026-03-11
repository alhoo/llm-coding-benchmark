# Evaluation Rubric: P07 - Word Ladder

## Total Points: 100

---

## 1. Correctness (55 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Standard path exists | 15 | `hit→hot→dot→dog→cog` = 5 |
| No path (endWord not in list) | 15 | Returns 0 |
| No path (disconnected) | 10 | endWord in list but unreachable |
| Single-step transformation | 10 | beginWord differs by one letter from endWord |
| Long path | 5 | Chain of 8+ transformations |

---

## 2. Algorithm (35 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| BFS (guarantees shortest path) | 35 | Correct and optimal |
| DFS with backtracking | 10 | Finds A path but not necessarily shortest |
| Brute force / no graph model | 0 | No credit |

**Note**: BFS is required because it finds the *shortest* path. DFS may find a longer path.

---

## 3. Code Quality (10 points)

### Efficiency of Neighbor Generation (5 points)
- ✅ **5 points**: Replace each character position with a-z, check against wordSet
- ⚠️ **3 points**: Compare every word in list to current word (O(L × |list|) per step)
- ❌ **0 points**: Recomputes transformations redundantly

### Visited Set (5 points)
- ✅ **5 points**: Uses a visited set to avoid revisiting words
- ❌ **0 points**: Revisits words (infinite loop risk)

---

## Common LLM Failures

### ❌ Failure Pattern 1: Uses DFS Instead of BFS

```python
def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    # ❌ DFS finds A path but not necessarily the SHORTEST
    def dfs(word, depth):
        if word == end_word:
            return depth
        ...
```

**Score**: 38/100 (Fails shortest-path test cases)

---

### ❌ Failure Pattern 2: No Visited Set

```python
while queue:
    word, steps = queue.popleft()
    for neighbor in get_neighbors(word, word_set):
        queue.append((neighbor, steps + 1))  # ❌ Revisits words!
```

**Score**: 0/100 (Infinite loop or TLE)

---

## ✅ Reference Solution

```python
from collections import deque

def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, steps = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word == end_word:
                    return steps + 1
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, steps + 1))

    return 0
```

**Score**: 100/100
