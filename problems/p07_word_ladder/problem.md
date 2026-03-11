# Problem P07: Word Ladder

## Problem Statement

A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord → s1 → s2 → ... → sk` such that:

- Every adjacent pair of words differs by a **single letter**.
- Every `si` for `1 <= i <= k` is in `wordList`.
- `sk == endWord`

Given `beginWord`, `endWord`, and `wordList`, return the **number of words in the shortest transformation sequence** from `beginWord` to `endWord`, or `0` if no such sequence exists.

---

## Examples

### Example 1:
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: hit → hot → dot → dog → cog (5 words)
```

### Example 2:
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: "cog" is not in wordList, so no transformation is possible.
```

---

## Constraints

- `1 <= beginWord.length <= 10`
- `endWord.length == beginWord.length`
- `1 <= wordList.length <= 5000`
- `wordList[i].length == beginWord.length`
- `beginWord`, `endWord`, and `wordList[i]` consist of lowercase English letters.
- `beginWord != endWord`
- All words in `wordList` are unique.

---

## Hints

1. Model as a graph: each word is a node, edge exists if words differ by one letter.
2. **BFS** finds the shortest path (minimum transformations).
3. To find neighbors efficiently, replace each character with `'a'`–`'z'` and check against a set.
4. Use a visited set to avoid revisiting words.

---

## Function Signature

### Python
```python
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (55 points) — All test cases pass
2. **Algorithm** (35 points) — Uses BFS (not DFS/brute force)
3. **Code Quality** (10 points) — Efficient neighbor generation, clean code
