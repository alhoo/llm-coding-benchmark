# Evaluation Rubric: P10 - Concurrent Task Scheduler

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Concurrency limit respected | 15 | Never more than `max_concurrent` tasks run simultaneously |
| Priority ordering | 15 | Higher priority tasks run before lower priority ones |
| FIFO tie-breaking | 10 | Equal priority → submission order |
| All tasks complete | 10 | No tasks lost, `shutdown()` waits for all |

---

## 2. Concurrency Safety (30 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| No race conditions | 15 | Concurrent `schedule()` calls are safe |
| No busy-waiting | 10 | Uses `asyncio` primitives, not polling loops |
| Correct shutdown | 5 | `shutdown()` drains queue before returning |

---

## 3. Code Quality (20 points)

### asyncio Primitives (10 points)
- ✅ **10 points**: Uses `asyncio.PriorityQueue`, `asyncio.Semaphore`, `asyncio.Future` correctly
- ⚠️ **5 points**: Works but uses `asyncio.sleep(0)` polling or threading primitives
- ❌ **0 points**: Busy-wait loops, incorrect primitive usage

### Design Clarity (10 points)
- ✅ **10 points**: Clean worker loop, clear separation of scheduling and execution
- ⚠️ **5 points**: Works but monolithic or hard to follow
- ❌ **0 points**: Tangled coroutines, unclear state management

---

## Common LLM Failures

### ❌ Failure Pattern 1: No Priority Queue (FIFO Only)

```python
class TaskScheduler:
    def __init__(self, max_concurrent):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue = asyncio.Queue()  # ❌ FIFO, ignores priority
```

**Score**: 50/100 (Concurrency correct, priority ordering wrong)

---

### ❌ Failure Pattern 2: Busy-Wait

```python
async def schedule(self, task_id, priority, coro):
    while self.running >= self.max_concurrent:
        await asyncio.sleep(0.01)  # ❌ Busy-wait
    ...
```

**Score**: 50/100 (Works but violates "no busy-waiting" requirement)

---

### ❌ Failure Pattern 3: Coroutine Not Awaitable After Queuing

```python
# If coro is put in queue but the worker tries to await it later,
# it needs to still be awaitable (not already consumed)
heapq.heappush(self.heap, (priority, coro))
# ❌ Coroutines can only be awaited once; need asyncio.ensure_future or similar
```

---

## ✅ Reference Solution

```python
import asyncio
from typing import Any, Coroutine

class TaskScheduler:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._counter = 0
        self._worker_task: asyncio.Task | None = None
        self._shutdown_event = asyncio.Event()

    async def _worker(self):
        while not self._shutdown_event.is_set() or not self._queue.empty():
            try:
                neg_priority, seq, task_id, coro, future = \
                    await asyncio.wait_for(self._queue.get(), timeout=0.05)
            except asyncio.TimeoutError:
                continue
            await self._semaphore.acquire()
            async def run(c, f):
                try:
                    result = await c
                    f.set_result(result)
                except Exception as e:
                    f.set_exception(e)
                finally:
                    self._semaphore.release()
            asyncio.create_task(run(coro, future))
            self._queue.task_done()

    async def schedule(self, task_id: str, priority: int, coro: Coroutine) -> Any:
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker())
        loop = asyncio.get_event_loop()
        future: asyncio.Future = loop.create_future()
        self._counter += 1
        await self._queue.put((-priority, self._counter, task_id, coro, future))
        return await future

    async def shutdown(self) -> None:
        self._shutdown_event.set()
        if self._worker_task:
            await self._worker_task
```

**Score**: 100/100
