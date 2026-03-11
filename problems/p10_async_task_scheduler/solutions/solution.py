"""
Reference solution for Concurrent Task Scheduler.
Uses asyncio.PriorityQueue + asyncio.Semaphore for concurrency control.
Time Complexity: O(log k) per schedule call (heap push)
Space Complexity: O(k) where k is number of queued tasks
"""

import asyncio
from typing import Any, Coroutine


class TaskScheduler:
    """
    Async task scheduler with priority ordering and concurrency limits.

    - Tasks with higher priority values execute first.
    - Equal-priority tasks execute in FIFO order (submission order).
    - At most max_concurrent tasks run simultaneously.
    - No busy-waiting: uses asyncio primitives throughout.
    """

    def __init__(self, max_concurrent: int):
        self._max_concurrent = max_concurrent
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._counter = 0
        self._active_tasks: set[asyncio.Task] = set()
        self._worker_task: asyncio.Task | None = None
        self._shutdown = False

    def _ensure_worker(self) -> None:
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker())

    async def _worker(self) -> None:
        while True:
            try:
                item = await asyncio.wait_for(self._queue.get(), timeout=0.05)
            except asyncio.TimeoutError:
                if self._shutdown and self._queue.empty():
                    break
                continue

            neg_priority, seq, task_id, coro, future = item

            await self._semaphore.acquire()

            async def _run(c: Coroutine, f: asyncio.Future) -> None:
                try:
                    result = await c
                    if not f.done():
                        f.set_result(result)
                except Exception as exc:
                    if not f.done():
                        f.set_exception(exc)
                finally:
                    self._semaphore.release()

            task = asyncio.create_task(_run(coro, future))
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)
            self._queue.task_done()

    async def schedule(self, task_id: str, priority: int, coro: Coroutine) -> Any:
        """
        Schedule a coroutine for execution.

        Args:
            task_id: Identifier for this task (for logging/debugging)
            priority: Execution priority (higher = runs sooner)
            coro: Coroutine to execute

        Returns:
            The return value of the coroutine.
        """
        self._ensure_worker()
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        self._counter += 1
        await self._queue.put((-priority, self._counter, task_id, coro, future))
        return await future

    async def shutdown(self) -> None:
        """Wait for all queued and running tasks to complete."""
        self._shutdown = True
        await self._queue.join()
        if self._active_tasks:
            await asyncio.gather(*self._active_tasks, return_exceptions=True)
        if self._worker_task and not self._worker_task.done():
            await self._worker_task


if __name__ == "__main__":
    import asyncio

    async def main():
        scheduler = TaskScheduler(max_concurrent=2)
        order: list[str] = []

        async def work(name: str) -> str:
            await asyncio.sleep(0.01)
            order.append(name)
            return name

        t_low = asyncio.create_task(scheduler.schedule("low", 1, work("low")))
        t_high = asyncio.create_task(scheduler.schedule("high", 10, work("high")))
        t_mid = asyncio.create_task(scheduler.schedule("mid", 5, work("mid")))

        results = await asyncio.gather(t_low, t_high, t_mid)
        await scheduler.shutdown()

        assert set(results) == {"low", "high", "mid"}
        print(f"Execution order: {order}")
        print("All tests passed!")

    asyncio.run(main())
