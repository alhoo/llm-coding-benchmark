"""
Reference solution for Regular Expression Matching.
Uses 2D dynamic programming.
Time Complexity: O(m * n) where m = len(s), n = len(p)
Space Complexity: O(m * n)
"""


def is_match(s: str, p: str) -> bool:
    """
    Determine if string s matches pattern p with '.' and '*' wildcards.

    dp[i][j] = True if s[0..i-1] matches p[0..j-1].

    Transitions:
    - p[j-1] is a letter or '.': dp[i][j] = dp[i-1][j-1] AND chars match
    - p[j-1] is '*':
        - Zero occurrences of p[j-2]: dp[i][j] = dp[i][j-2]
        - One more occurrence:        dp[i][j] |= dp[i-1][j] AND p[j-2] matches s[i-1]

    Base cases:
    - dp[0][0] = True (empty string matches empty pattern)
    - dp[0][j]: only patterns like "a*b*c*" can match an empty string

    Args:
        s: Input string (lowercase letters only)
        p: Pattern string (lowercase letters, '.', '*')

    Returns:
        True if s fully matches p, False otherwise.

    Example:
        >>> is_match("aa", "a*")
        True
        >>> is_match("mississippi", "mis*is*p*.")
        False
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]
                if p[j - 2] == "." or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == "." or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


if __name__ == "__main__":
    assert is_match("aa", "a") is False
    assert is_match("aa", "a*") is True
    assert is_match("ab", ".*") is True
    assert is_match("aab", "c*a*b") is True
    assert is_match("mississippi", "mis*is*p*.") is False
    assert is_match("", "a*") is True
    assert is_match("", "") is True
    assert is_match("a", "") is False
    print("All tests passed!")
