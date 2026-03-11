# Evaluation Rubric: P14 - Suffix Array, LCP Array & Distinct Substrings

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Suffix array — basic | 10 | "banana" → [5, 3, 1, 0, 4, 2] |
| Suffix array — all same | 5 | "aaaa" → [3, 2, 1, 0] |
| Suffix array — all unique | 5 | "abcde" → [0, 1, 2, 3, 4] |
| LCP array — correct values | 10 | Matches expected LCP for all test strings |
| LCP array — first element zero | 2 | lcp[0] == 0 always |
| LCP array — bounded values | 3 | lcp[i] ≤ min suffix length |
| Distinct substrings formula | 10 | Correct count via n*(n+1)/2 - sum(lcp) |
| Cross-check with brute force | 5 | Matches set-based counting on small strings |

**Scoring**:
- Pass all: 50 points
- Fail 1-2 cases: 35 points
- Fail 3-4 cases: 20 points
- Fail 5+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Suffix Array: Expected O(n log² n) or better

| Implementation | Points | Description |
|----------------|--------|-------------|
| Prefix doubling with radix sort — O(n log n) | 35 | Optimal |
| Prefix doubling with comparison sort — O(n log² n) | 30 | Standard competitive programming approach |
| SA-IS — O(n) | 35 | Linear but complex to implement |
| Naïve sort of all suffixes — O(n² log n) | 5 | Correct but too slow |
| Brute force enumeration | 0 | Unacceptable |

### LCP Array: Expected O(n)

| Implementation | Points | Description |
|----------------|--------|-------------|
| Kasai's algorithm — O(n) | (included above) | Optimal |
| Pairwise comparison — O(n²) | -10 | Too slow, loses points |

### Distinct Substrings: Expected formula-based

| Implementation | Points | Description |
|----------------|--------|-------------|
| n*(n+1)/2 - sum(lcp) | (included above) | O(n) after SA/LCP |
| Brute force set — O(n³) | -15 | Unacceptable for n=100,000 |

**Verification Method**:
- Timing test: n=100,000 random string should complete in < 10 seconds
- Timing test: n=100,000 repetitive string should complete in < 10 seconds

---

## 3. Code Quality (15 points)

### Algorithm Design (8 points)
- ✅ **8 points**: Clean prefix doubling with clear rank assignment, proper Kasai's implementation
- ⚠️ **4 points**: Works but rank update logic is convoluted or uses unnecessary data structures
- ❌ **0 points**: Incorrect algorithm or missing components

### Edge Cases (4 points)
- ✅ **4 points**: Handles empty string, single char, all-same characters, all-unique characters
- ❌ **0 points**: Crashes on edge cases

### Best Practices (3 points)
- ✅ **3 points**: Clean separation of SA/LCP/counting, proper variable names
- ❌ **0 points**: Monolithic function, cryptic variable names

---

## Common LLM Failures

### ❌ Failure Pattern 1: Naïve Suffix Sort

```python
def build_suffix_array(s):
    # ❌ O(n² log n) — sorts n suffixes of average length n/2
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort()
    return [idx for _, idx in suffixes]
```

**Score**: 40/100 (Correct but TLE on n=100,000)

---

### ❌ Failure Pattern 2: Wrong LCP — Pairwise Comparison Instead of Kasai's

```python
def build_lcp_array(s, sa):
    lcp = [0] * len(sa)
    for i in range(1, len(sa)):
        a, b = sa[i-1], sa[i]
        k = 0
        # ❌ O(n) per pair → O(n²) total
        while a + k < len(s) and b + k < len(s) and s[a+k] == s[b+k]:
            k += 1
        lcp[i] = k
    return lcp
```

**Score**: 55/100 (Correct but O(n²) LCP construction)

---

### ❌ Failure Pattern 3: Off-by-One in Kasai's Algorithm

```python
def build_lcp_array(s, sa):
    n = len(s)
    inv = [0] * n
    for i in range(n):
        inv[sa[i]] = i
    lcp = [0] * n
    k = 0
    for i in range(n):
        if inv[i] == 0:
            # ❌ Forgets to reset k to 0 here
            continue
        j = sa[inv[i] - 1]
        while i + k < n and j + k < n and s[i+k] == s[j+k]:
            k += 1
        lcp[inv[i]] = k
        k = max(k - 1, 0)  # Sometimes written as k -= 1 without the max
    return lcp
```

**Score**: 70/100 (Subtle off-by-one that may produce wrong LCP values for some inputs)

---

### ❌ Failure Pattern 4: Brute-Force Distinct Substring Counting

```python
def count_distinct_substrings(s):
    # ❌ O(n³) — generates all substrings and deduplicates via set
    return len({s[i:j] for i in range(len(s)) for j in range(i+1, len(s)+1)})
```

**Score**: 35/100 (Correct for small inputs, memory/time explosion on large inputs)

---

### ❌ Failure Pattern 5: Rank Update Bug in Prefix Doubling

```python
# During the doubling step, ranks must be reassigned based on
# (rank[i], rank[i+k]) pairs. A common bug:
for i in range(1, n):
    if rank[sa[i]] != rank[sa[i-1]]:  # ❌ Compares single rank, not the pair
        new_rank += 1
    tmp[sa[i]] = new_rank
```

**Score**: 20/100 (Produces incorrect suffix array for most inputs)

---

## ✅ Reference Solution

```python
def build_suffix_array(s):
    n = len(s)
    if n == 0:
        return []
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while k < n:
        def compare_key(i):
            return (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=compare_key)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]]
            if compare_key(sa[i]) != compare_key(sa[i - 1]):
                tmp[sa[i]] += 1
        rank[:] = tmp
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa

def build_lcp_array(s, suffix_array):
    n = len(s)
    if n == 0:
        return []
    inv = [0] * n
    for i, sa_val in enumerate(suffix_array):
        inv[sa_val] = i
    lcp = [0] * n
    k = 0
    for i in range(n):
        if inv[i] == 0:
            k = 0
            continue
        j = suffix_array[inv[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[inv[i]] = k
        if k > 0:
            k -= 1
    return lcp

def count_distinct_substrings(s):
    n = len(s)
    if n == 0:
        return 0
    sa = build_suffix_array(s)
    lcp = build_lcp_array(s, sa)
    return n * (n + 1) // 2 - sum(lcp)
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(n log² n) for SA, O(n) for LCP
- ✅ Code Quality: Clean, well-structured
