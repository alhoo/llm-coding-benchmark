# Problem P03: Binary Tree Serialization

## Problem Statement

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored or transmitted and reconstructed later.

Design an algorithm to **serialize** and **deserialize** a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized into a string and this string can be deserialized into the original tree structure.

Implement the `Codec` class:

- `string serialize(TreeNode root)` — Encodes a tree to a single string.
- `TreeNode deserialize(string data)` — Decodes the encoded data back to tree.

---

## Examples

### Example 1:
```
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
Explanation: The serialized form is reconstructed into the same tree.

    1
   / \
  2   3
     / \
    4   5
```

### Example 2:
```
Input: root = []
Output: []
```

---

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

---

## Hints

1. BFS (level-order) traversal produces a natural serialization format.
2. Alternatively, preorder DFS with null markers also works well.
3. When deserializing, use a queue to match parent nodes to their children.
4. Handle null nodes explicitly in your serialized string.

---

## TreeNode Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## Function Signature

### Python
```python
class Codec:
    def serialize(self, root: TreeNode) -> str:
        pass

    def deserialize(self, data: str) -> TreeNode:
        pass
```

---

## Evaluation Criteria

1. **Correctness** (60 points) — serialize → deserialize produces identical tree
2. **Completeness** (30 points) — Handles all edge cases (empty tree, single node, skewed tree)
3. **Code Quality** (10 points) — Clean, readable implementation
