"""
Reference solution for Suffix Array, LCP Array & Distinct Substrings.

- build_suffix_array: O(n log^2 n) via prefix doubling with built-in sort
- build_lcp_array: O(n) via Kasai's algorithm
- count_distinct_substrings: O(n log^2 n) dominated by suffix array construction

The suffix array SA is the permutation of [0..n-1] such that
s[SA[0]:] < s[SA[1]:] < ... < s[SA[n-1]:] lexicographically.

The LCP array stores the length of the longest common prefix between
consecutive suffixes in the sorted order: lcp[i] = LCP(s[SA[i-1]:], s[SA[i]:]).
By convention lcp[0] = 0.
"""


def build_suffix_array(s: str) -> list[int]:
    """
    Construct the suffix array using prefix doubling.

    Assign each suffix an initial rank equal to its first character's ordinal.
    Then repeatedly sort by (rank[i], rank[i + k]) pairs, doubling k each
    iteration, until all ranks are unique.
    """
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


def build_lcp_array(s: str, suffix_array: list[int]) -> list[int]:
    """
    Kasai's algorithm: compute the LCP array in O(n).

    Key insight: if we know LCP between suffix SA[rank[i]-1] and SA[rank[i]]
    is h, then the LCP between suffix SA[rank[i+1]-1] and SA[rank[i+1]] is
    at least h-1. This lets us traverse in text order and amortize comparisons.
    """
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


def count_distinct_substrings(s: str) -> int:
    """
    Count distinct non-empty substrings using SA + LCP.

    Total substrings = n*(n+1)/2. Each lcp[i] value represents shared prefixes
    (duplicates) between adjacent sorted suffixes. Subtracting removes
    double-counted substrings.
    """
    n = len(s)
    if n == 0:
        return 0
    sa = build_suffix_array(s)
    lcp = build_lcp_array(s, sa)
    total = n * (n + 1) // 2
    return total - sum(lcp)


if __name__ == "__main__":
    assert build_suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert build_lcp_array("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]
    assert count_distinct_substrings("banana") == 15
    assert count_distinct_substrings("abab") == 7
    assert count_distinct_substrings("aaaa") == 4
    assert count_distinct_substrings("abcde") == 15
    print("All tests passed!")
