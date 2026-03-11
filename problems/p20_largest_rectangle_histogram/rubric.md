# Evaluation Rubric: P20 - Largest Rectangle in Histogram

## Total Points: 100

---

## 1. Correctness (50 points)

| Category | Points | Description |
|----------|--------|-------------|
| Basic cases | 15 | Example histograms (e.g. [2,1,5,6,2,3] → 10) |
| Edge cases | 15 | Single bar, all same height, strictly increasing/decreasing |
| Complex patterns | 20 | Valley, two peaks, tall-narrow, zeros |

**Scoring**:
- Pass all: 50 points
- Fail 1–2 cases: 35 points
- Fail 3+ cases: 0 points

---

## 2. Time Complexity (40 points)

### Expected: O(n)

| Implementation | Points | Description |
|----------------|--------|-------------|
| Monotonic stack | 40 | Optimal O(n) — each bar pushed/popped at most once |
| Divide & conquer | 30 | O(n log n) — correct but not optimal |
| Naive expand left/right | 0 | O(n²) — fails timing test |

**Verification**:
- Timing test: 50,000 bars must complete in < 1.5 seconds
- O(n²) solutions typically take 50+ seconds and fail

---

## 3. Code Quality (10 points)

- **5 points**: Clear variable names, stack logic readable
- **3 points**: Works but obscure
- **0 points**: Unreadable or incorrect structure

---

## Common LLM Failures

### ❌ Failure 1: Submitting O(n²) Naive Solution

Keeping the expand-left/expand-right approach. Correct but fails the time complexity test.

**Score**: 50/100 (correctness only)

---

### ❌ Failure 2: Off-by-One in Monotonic Stack

Incorrect width calculation when popping from stack (e.g. `width = i - h_idx` instead of `width = i - left - 1`).

**Score**: 0–35/100 (fails correctness)

---

### ❌ Failure 3: Forgetting to Process Remaining Stack

After the main loop, bars still in the stack have right boundary = n. Must process them.

**Score**: 35–50/100 (fails some test cases)

---

## ✅ Reference Solution Pattern

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack = []
    max_area = 0
    n = len(heights)

    for i in range(n):
        while stack and heights[i] < heights[stack[-1]]:
            h_idx = stack.pop()
            h = heights[h_idx]
            left = stack[-1] if stack else -1
            width = i - left - 1
            max_area = max(max_area, h * width)
        stack.append(i)

    while stack:
        h_idx = stack.pop()
        h = heights[h_idx]
        left = stack[-1] if stack else -1
        width = n - left - 1
        max_area = max(max_area, h * width)

    return max_area
```
