"""
Reference solution for Word Ladder.
Uses BFS to find the shortest transformation sequence.
Time Complexity: O(M² × N) where M = word length, N = number of words
Space Complexity: O(M² × N)
"""

from collections import deque


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """
    Return the number of words in the shortest transformation sequence
    from begin_word to end_word, or 0 if no such sequence exists.

    Each step changes exactly one letter, and each intermediate word
    must be in word_list.

    Args:
        begin_word: Starting word
        end_word: Target word
        word_list: List of valid intermediate/target words

    Returns:
        Length of shortest path (number of words), or 0 if unreachable.

    Example:
        >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
        5
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue: deque[tuple[str, int]] = deque([(begin_word, 1)])
    visited: set[str] = {begin_word}

    while queue:
        word, steps = queue.popleft()
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c == word[i]:
                    continue
                next_word = word[:i] + c + word[i + 1:]
                if next_word == end_word:
                    return steps + 1
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, steps + 1))

    return 0


if __name__ == "__main__":
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2
    print("All tests passed!")
