# Problem P14: Suffix Array, LCP Array & Distinct Substrings

## Problem Statement

Given a string `s` consisting of lowercase English letters, implement three functions:

1. **`build_suffix_array(s)`** — Construct the suffix array of `s`. The suffix array is a sorted array of all suffix indices `[0, 1, ..., n-1]` where suffix `i` is the substring `s[i:]`. Sort lexicographically. Must run in **O(n log² n)** time or better.

2. **`build_lcp_array(s, suffix_array)`** — Given the string and its suffix array, construct the LCP (Longest Common Prefix) array using **Kasai's algorithm** in O(n) time. `lcp[i]` is the length of the longest common prefix between the suffixes at positions `suffix_array[i]` and `suffix_array[i-1]` in the sorted order. By convention, `lcp[0] = 0`.

3. **`count_distinct_substrings(s)`** — Return the number of **distinct non-empty substrings** of `s`. Use the suffix array and LCP array to compute this in O(n log² n) time or better (not by brute-force enumeration).

   The formula is: `n*(n+1)/2 - sum(lcp)` where `n = len(s)`.

---

## Examples

### Example 1:
```
Input: s = "banana"
Suffix array: [5, 3, 1, 0, 4, 2]
  Sorted suffixes:
    5: "a"
    3: "ana"
    1: "anana"
    0: "banana"
    4: "na"
    2: "nana"

LCP array: [0, 1, 3, 0, 0, 2]
  lcp[0] = 0 (no predecessor)
  lcp[1] = 1 ("a" vs "ana" → "a")
  lcp[2] = 3 ("ana" vs "anana" → "ana")
  lcp[3] = 0 ("anana" vs "banana" → "")
  lcp[4] = 0 ("banana" vs "na" → "")
  lcp[5] = 2 ("na" vs "nana" → "na")

Distinct substrings: 6*7/2 - (0+1+3+0+0+2) = 21 - 6 = 15
```

### Example 2:
```
Input: s = "abab"
Suffix array: [2, 0, 3, 1]
  Sorted suffixes:
    2: "ab"
    0: "abab"
    3: "b"
    1: "bab"

LCP array: [0, 2, 0, 1]

Distinct substrings: 4*5/2 - (0+2+0+1) = 10 - 3 = 7
The 7 distinct substrings: "a", "ab", "aba", "abab", "b", "ba", "bab"
```

### Example 3:
```
Input: s = "aaaa"
Suffix array: [3, 2, 1, 0]
LCP array: [0, 1, 2, 3]
Distinct substrings: 4*5/2 - (0+1+2+3) = 10 - 6 = 4
The 4 distinct substrings: "a", "aa", "aaa", "aaaa"
```

### Example 4:
```
Input: s = "abcde"
Suffix array: [0, 1, 2, 3, 4]
LCP array: [0, 0, 0, 0, 0]
Distinct substrings: 5*6/2 - 0 = 15
All substrings are distinct (no repeated characters).
```

---

## Constraints

- `1 <= len(s) <= 100,000`
- `s` consists only of lowercase English letters (`a`-`z`).

---

## Hints

1. **Suffix Array Construction**: Use the "prefix doubling" approach. Assign initial ranks based on character values. Repeatedly sort suffixes by their (rank, rank+k) pairs for k = 1, 2, 4, 8, ... until all ranks are unique. Use stable sorting (or radix sort) for each doubling step.

2. **Kasai's Algorithm**: Traverse suffixes in original order (not sorted order). Maintain a variable `k` for the current LCP length. For suffix `i`, find its position in the suffix array, compare it with its predecessor, and reuse the previous LCP value minus one as a lower bound.

3. **Distinct Substrings**: A string of length `n` has `n*(n+1)/2` total substrings. The LCP array tells you how many are duplicated with the previous suffix in sorted order. Subtracting `sum(lcp)` gives the distinct count.

---

## Function Signature

### Python
```python
def build_suffix_array(s: str) -> list[int]:
    pass

def build_lcp_array(s: str, suffix_array: list[int]) -> list[int]:
    pass

def count_distinct_substrings(s: str) -> int:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All three functions return correct results on all test cases
2. **Time Complexity** (35 points) — Suffix array in O(n log² n) or better, LCP in O(n), distinct count using the formula
3. **Code Quality** (15 points) — Clear rank/doubling logic, proper Kasai's implementation, clean integration
