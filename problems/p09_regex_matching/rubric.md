# Evaluation Rubric: P09 - Regular Expression Matching

## Total Points: 100

---

## 1. Correctness (60 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| No wildcards | 10 | `"aa", "a"` → false |
| `*` zero times | 10 | `"b", "a*b"` → true |
| `*` multiple times | 10 | `"aa", "a*"` → true |
| `.` wildcard | 10 | `"ab", ".*"` → true |
| Complex pattern | 10 | `"aab", "c*a*b"` → true |
| Hard case | 10 | `"mississippi", "mis*is*p*."` → false |

---

## 2. Algorithm (30 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| 2D DP — O(mn) | 30 | Optimal |
| Memoized recursion — O(mn) | 25 | Equivalent complexity, slightly less clean |
| Pure recursion — O(2^(m+n)) | 0 | Exponential — unacceptable |

---

## 3. Code Quality (10 points)

### State Transitions (5 points)
- ✅ **5 points**: Correct handling of all three cases: plain char, `.`, and `*`
- ⚠️ **3 points**: Works but `*` case logic is convoluted
- ❌ **0 points**: Incorrect base cases for DP table

### Readability (5 points)
- ✅ **5 points**: Clear DP table definition, meaningful variable names
- ❌ **0 points**: Cryptic one-liners without comments

---

## Common LLM Failures

### ❌ Failure Pattern 1: Exponential Recursion

```python
def is_match(s, p):
    if not p:
        return not s
    first_match = bool(s) and p[0] in {s[0], '.'}
    if len(p) >= 2 and p[1] == '*':
        # ❌ No memoization — exponential time
        return is_match(s, p[2:]) or (first_match and is_match(s[1:], p))
    return first_match and is_match(s[1:], p[1:])
```

**Score**: 60/100 (Correct for small inputs, TLE on large)

---

### ❌ Failure Pattern 2: Wrong Base Case for `*`

```python
# dp[0][j] should handle patterns like "a*b*c*" matching empty string
# Many LLMs forget to initialize this correctly
dp = [[False] * (len(p)+1) for _ in range(len(s)+1)]
dp[0][0] = True
# ❌ Forgets: dp[0][j] = dp[0][j-2] when p[j-1] == '*'
```

---

## ✅ Reference Solution

```python
def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]  # '*' matches zero occurrences
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]  # '*' matches one more
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

**Score**: 100/100
