# Problem P09: Regular Expression Matching

## Problem Statement

Given an input string `s` and a pattern `p`, implement regular expression matching with support for `'.'` and `'*'` where:

- `'.'` matches any single character.
- `'*'` matches zero or more of the preceding element.

The matching should cover the **entire** input string (not partial).

---

## Examples

### Example 1:
```
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
```

### Example 2:
```
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of 'a', so "a*" matches "aa".
```

### Example 3:
```
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" matches any sequence of characters.
```

### Example 4:
```
Input: s = "aab", p = "c*a*b"
Output: true
Explanation: 'c' repeated 0 times, 'a' repeated 2 times, then 'b'.
```

### Example 5:
```
Input: s = "mississippi", p = "mis*is*p*."
Output: false
```

---

## Constraints

- `1 <= s.length <= 20`
- `1 <= p.length <= 30`
- `s` contains only lowercase English letters.
- `p` contains only lowercase English letters, `'.'`, and `'*'`.
- It is guaranteed that for each occurrence of `'*'`, there will be a previous valid character to match.

---

## Hints

1. The recursive approach has exponential time due to overlapping subproblems.
2. Use **2D dynamic programming**: `dp[i][j]` = does `s[0..i-1]` match `p[0..j-1]`?
3. Cases:
   - `p[j-1]` is a letter or `.`: `dp[i][j] = dp[i-1][j-1] AND (s[i-1] matches p[j-1])`
   - `p[j-1]` is `*`: `dp[i][j] = dp[i][j-2]` (zero occurrences) OR `dp[i-1][j] AND (s[i-1] matches p[j-2])`

---

## Function Signature

### Python
```python
def is_match(s: str, p: str) -> bool:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (60 points) — All test cases pass
2. **Algorithm** (30 points) — Dynamic programming (not exponential recursion)
3. **Code Quality** (10 points) — Clear state transitions, readable DP table
