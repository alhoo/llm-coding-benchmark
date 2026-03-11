"""
Test harness for Binary Tree Serialization problem (Python)
"""

import importlib.util
import json
import pytest
from pathlib import Path
from collections import deque


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p03_binary_tree_codec_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def build_tree(level_order: list, TreeNode):
    """Build a binary tree from a level-order list (None for missing nodes)."""
    if not level_order:
        return None

    root = TreeNode(level_order[0])
    queue = deque([root])
    i = 1
    while queue and i < len(level_order):
        node = queue.popleft()
        if i < len(level_order) and level_order[i] is not None:
            node.left = TreeNode(level_order[i])
            queue.append(node.left)
        i += 1
        if i < len(level_order) and level_order[i] is not None:
            node.right = TreeNode(level_order[i])
            queue.append(node.right)
        i += 1
    return root


def trees_equal(a, b) -> bool:
    """Recursively compare two trees for structural and value equality."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and trees_equal(a.left, b.left) and trees_equal(a.right, b.right)


class TestBinaryTreeCodec:
    """Test suite for Binary Tree Serialization problem."""

    @pytest.fixture
    def mod(self):
        return _load_solution()

    @pytest.fixture
    def codec(self, mod):
        return mod.Codec()

    @pytest.fixture
    def TreeNode(self, mod):
        return mod.TreeNode

    def test_empty_tree(self, codec):
        """Empty tree (None) round-trips correctly."""
        assert codec.deserialize(codec.serialize(None)) is None

    def test_single_node(self, codec, TreeNode):
        """Single node tree round-trips correctly."""
        root = TreeNode(42)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)

    def test_complete_tree(self, codec, TreeNode):
        """Complete binary tree round-trips correctly."""
        root = build_tree([1, 2, 3, None, None, 4, 5], TreeNode)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)

    def test_left_skewed(self, codec, TreeNode):
        """Left-skewed tree round-trips correctly."""
        root = build_tree([1, 2, None, 3, None, 4, None], TreeNode)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)

    def test_right_skewed(self, codec, TreeNode):
        """Right-skewed tree round-trips correctly."""
        root = build_tree([1, None, 2, None, 3, None, 4], TreeNode)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)

    def test_negative_values(self, codec, TreeNode):
        """Tree with negative values round-trips correctly."""
        root = build_tree([-10, -5, -1, None, None, -3, None], TreeNode)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, codec, TreeNode, case):
        """All JSON-defined test cases."""
        root = build_tree(case["tree"], TreeNode)
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root), f"Round-trip failed for '{case['name']}'"

    def test_deep_tree(self, codec, TreeNode):
        """Deep right-skewed tree (1000 nodes) round-trips correctly."""
        root = curr = TreeNode(0)
        for i in range(1, 1000):
            curr.right = TreeNode(i)
            curr = curr.right
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(result, root)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
