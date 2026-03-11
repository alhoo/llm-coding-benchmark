"""
Reference solution for Binary Tree Serialization.
Uses BFS (level-order) traversal.
Time Complexity: O(n) for both serialize and deserialize
Space Complexity: O(n)
"""

from collections import deque


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """
    Serializes/deserializes a binary tree using BFS level-order traversal.
    Null children are encoded as 'null'.
    Nodes are comma-separated.
    """

    def serialize(self, root: TreeNode | None) -> str:
        if root is None:
            return ""

        result: list[str] = []
        queue: deque[TreeNode | None] = deque([root])

        while queue:
            node = queue.popleft()
            if node is None:
                result.append("null")
            else:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)

        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode | None:
        if not data:
            return None

        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        queue: deque[TreeNode] = deque([root])
        i = 1

        while queue and i < len(tokens):
            node = queue.popleft()

            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1

            if i < len(tokens) and tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1

        return root


def trees_equal(a: TreeNode | None, b: TreeNode | None) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and trees_equal(a.left, b.left) and trees_equal(a.right, b.right)


if __name__ == "__main__":
    codec = Codec()

    root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    assert trees_equal(codec.deserialize(codec.serialize(root)), root)

    assert codec.deserialize(codec.serialize(None)) is None

    single = TreeNode(42)
    assert trees_equal(codec.deserialize(codec.serialize(single)), single)

    print("All tests passed!")
