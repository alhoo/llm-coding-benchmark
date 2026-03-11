# Evaluation Rubric: P03 - Binary Tree Serialization

## Total Points: 100

---

## 1. Correctness (60 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Complete binary tree | 10 | Balanced tree with all levels filled |
| Skewed tree (left) | 10 | All nodes on left side |
| Skewed tree (right) | 10 | All nodes on right side |
| Single node | 10 | Root only |
| Empty tree | 10 | `None` root |
| Tree with negative values | 10 | Negative node values |

**Scoring**:
- Pass all: 60 points
- Fail 1 case: 45 points
- Fail 2 cases: 25 points
- Fail 3+ cases: 0 points

---

## 2. Completeness / Edge Cases (30 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Empty tree round-trips | 10 | `serialize(None)` → `deserialize(...)` = `None` |
| Single node round-trips | 10 | Root-only tree |
| Deep skewed tree | 10 | 1000+ node linear chain |

---

## 3. Code Quality (10 points)

### Clarity (5 points)
- ✅ **5 points**: Clear BFS or DFS approach, obvious null marker handling
- ⚠️ **3 points**: Works but convoluted parsing
- ❌ **0 points**: Obscure encoding scheme

### Robustness (5 points)
- ✅ **5 points**: Handles all edge cases without crashes
- ⚠️ **2 points**: Works for most cases, fragile parsing
- ❌ **0 points**: Crashes on empty or single-node trees

---

## Common LLM Failures

### ❌ Failure Pattern 1: Off-by-One in BFS Deserialization

```python
def deserialize(self, data: str) -> TreeNode:
    nodes = data.split(',')
    root = TreeNode(int(nodes[0]))
    queue = deque([root])
    i = 1
    while queue:
        node = queue.popleft()
        # ❌ Doesn't check if i is in bounds
        node.left = TreeNode(int(nodes[i])) if nodes[i] != 'null' else None
        node.right = TreeNode(int(nodes[i+1])) if nodes[i+1] != 'null' else None
        i += 2
```

---

### ❌ Failure Pattern 2: Doesn't Handle Empty Tree

```python
def serialize(self, root: TreeNode) -> str:
    # ❌ Crashes if root is None
    result = []
    queue = deque([root])
    ...
```

---

## ✅ Reference Solution

```python
from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return ''
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append('null')
        return ','.join(result)

    def deserialize(self, data):
        if not data:
            return None
        nodes = data.split(',')
        root = TreeNode(int(nodes[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(nodes):
            node = queue.popleft()
            if nodes[i] != 'null':
                node.left = TreeNode(int(nodes[i]))
                queue.append(node.left)
            i += 1
            if i < len(nodes) and nodes[i] != 'null':
                node.right = TreeNode(int(nodes[i]))
                queue.append(node.right)
            i += 1
        return root
```

**Score**: 100/100
