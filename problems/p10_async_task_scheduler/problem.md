# Problem P10: Concurrent Task Scheduler

## Problem Statement

Implement an **async task scheduler** that executes tasks with priorities and concurrency limits.

The `TaskScheduler` class must support:

- `TaskScheduler(max_concurrent: int)` — Initialize with a maximum number of concurrently running tasks.
- `async schedule(task_id: str, priority: int, coro: Coroutine) -> Any` — Schedule a coroutine for execution. Higher `priority` values run first (max-heap). Returns the result of the coroutine.
- `async shutdown() -> None` — Wait for all running/queued tasks to complete, then shut down.

**Requirements**:
- At most `max_concurrent` tasks run simultaneously.
- When a slot is free, the highest-priority pending task starts next.
- Equal priority tasks are executed in FIFO order.
- The scheduler is **thread-safe** (callable from multiple async contexts).

---

## Examples

```python
import asyncio

async def main():
    scheduler = TaskScheduler(max_concurrent=2)

    results = []

    async def work(name, delay):
        await asyncio.sleep(delay)
        results.append(name)
        return name

    # Schedule 4 tasks with only 2 concurrent slots
    t1 = asyncio.create_task(scheduler.schedule("t1", priority=1, coro=work("low",  0.1)))
    t2 = asyncio.create_task(scheduler.schedule("t2", priority=5, coro=work("high", 0.1)))
    t3 = asyncio.create_task(scheduler.schedule("t3", priority=3, coro=work("mid",  0.1)))
    t4 = asyncio.create_task(scheduler.schedule("t4", priority=5, coro=work("high2",0.1)))

    await asyncio.gather(t1, t2, t3, t4)
    await scheduler.shutdown()
    # Higher priority tasks complete before lower priority ones

asyncio.run(main())
```

---

## Constraints

- `1 <= max_concurrent <= 100`
- Tasks may be scheduled from multiple coroutines concurrently.
- `priority` is an integer; higher value = higher priority.
- Tasks must not be lost (every scheduled task must eventually run).
- No busy-waiting allowed.

---

## Hints

1. Use `asyncio.PriorityQueue` (negate priority for max-heap behavior).
2. Use a semaphore (`asyncio.Semaphore`) to limit concurrency.
3. Use `asyncio.Event` or `asyncio.Condition` to wake waiting tasks.
4. Store `(negated_priority, sequence_number, task_id, coro, future)` in the queue for FIFO tie-breaking.

---

## Function Signature

### Python
```python
import asyncio
from typing import Any, Coroutine

class TaskScheduler:
    def __init__(self, max_concurrent: int):
        pass

    async def schedule(self, task_id: str, priority: int, coro: Coroutine) -> Any:
        pass

    async def shutdown(self) -> None:
        pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — Tasks execute with correct priority ordering and concurrency limit
2. **Concurrency Safety** (30 points) — No race conditions, proper async primitives
3. **Code Quality** (20 points) — Idiomatic asyncio, no busy-waiting, clean shutdown
