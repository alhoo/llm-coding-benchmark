"""
Test harness for Concurrent Task Scheduler problem (Python)
"""

import asyncio
import importlib.util
import json
import time
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p10_async_task_scheduler_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestTaskScheduler:
    """Test suite for Concurrent Task Scheduler problem."""

    @pytest.fixture
    def scheduler_class(self):
        return _load_solution().TaskScheduler

    def test_all_tasks_complete(self, scheduler_class):
        """Every scheduled task must return its result."""
        async def run():
            scheduler = scheduler_class(max_concurrent=2)
            results = await asyncio.gather(
                scheduler.schedule("t1", 1, asyncio.sleep(0.01, result="a")),
                scheduler.schedule("t2", 2, asyncio.sleep(0.01, result="b")),
                scheduler.schedule("t3", 3, asyncio.sleep(0.01, result="c")),
            )
            await scheduler.shutdown()
            return results

        results = asyncio.run(run())
        assert set(results) == {"a", "b", "c"}

    def test_priority_ordering(self, scheduler_class):
        """With max_concurrent=1, tasks execute in priority order."""
        execution_order: list[str] = []

        async def run():
            scheduler = scheduler_class(max_concurrent=1)

            async def work(name: str) -> str:
                execution_order.append(name)
                return name

            # Schedule all at once; with concurrency=1, order should follow priority
            await asyncio.gather(
                scheduler.schedule("low",  1,  work("low")),
                scheduler.schedule("high", 10, work("high")),
                scheduler.schedule("mid",  5,  work("mid")),
            )
            await scheduler.shutdown()

        asyncio.run(run())
        assert execution_order.index("high") < execution_order.index("mid"), \
            f"Expected high before mid, got {execution_order}"
        assert execution_order.index("mid") < execution_order.index("low"), \
            f"Expected mid before low, got {execution_order}"

    def test_concurrency_limit(self, scheduler_class):
        """Never exceed max_concurrent running tasks simultaneously."""
        max_concurrent = 2
        running_count = 0
        max_seen = 0

        async def run():
            nonlocal running_count, max_seen
            scheduler = scheduler_class(max_concurrent=max_concurrent)

            async def work(name: str) -> str:
                nonlocal running_count, max_seen
                running_count += 1
                max_seen = max(max_seen, running_count)
                await asyncio.sleep(0.05)
                running_count -= 1
                return name

            tasks = [
                scheduler.schedule(f"t{i}", 1, work(f"t{i}"))
                for i in range(6)
            ]
            await asyncio.gather(*tasks)
            await scheduler.shutdown()

        asyncio.run(run())
        assert max_seen <= max_concurrent, (
            f"Exceeded concurrency limit: saw {max_seen} concurrent tasks, limit was {max_concurrent}"
        )

    def test_fifo_tiebreaking(self, scheduler_class):
        """Equal-priority tasks run in submission order."""
        execution_order: list[str] = []

        async def run():
            scheduler = scheduler_class(max_concurrent=1)

            async def work(name: str) -> str:
                execution_order.append(name)
                return name

            # Submit in order: first, second, third — all equal priority
            await asyncio.gather(
                scheduler.schedule("first",  5, work("first")),
                scheduler.schedule("second", 5, work("second")),
                scheduler.schedule("third",  5, work("third")),
            )
            await scheduler.shutdown()

        asyncio.run(run())
        assert execution_order == ["first", "second", "third"], (
            f"Expected FIFO order, got {execution_order}"
        )

    def test_return_values(self, scheduler_class):
        """schedule() returns the coroutine's return value."""
        async def run():
            scheduler = scheduler_class(max_concurrent=3)

            async def compute(x: int) -> int:
                await asyncio.sleep(0.001)
                return x * x

            results = await asyncio.gather(
                scheduler.schedule("sq2", 1, compute(2)),
                scheduler.schedule("sq3", 1, compute(3)),
                scheduler.schedule("sq4", 1, compute(4)),
            )
            await scheduler.shutdown()
            return results

        results = asyncio.run(run())
        assert set(results) == {4, 9, 16}

    def test_no_busy_wait(self, scheduler_class):
        """
        Scheduler should not spin/busy-wait: CPU usage during idle should be minimal.
        We test this by checking that a long-sleeping task doesn't monopolize event loop.
        """
        async def run():
            scheduler = scheduler_class(max_concurrent=2)

            async def slow_task():
                await asyncio.sleep(0.2)
                return "done"

            async def fast_task():
                await asyncio.sleep(0.01)
                return "fast"

            t1 = asyncio.create_task(scheduler.schedule("slow", 1, slow_task()))
            t2 = asyncio.create_task(scheduler.schedule("fast", 10, fast_task()))

            start = time.perf_counter()
            fast_result = await t2
            fast_elapsed = time.perf_counter() - start

            await t1
            await scheduler.shutdown()
            return fast_elapsed, fast_result

        fast_elapsed, fast_result = asyncio.run(run())
        assert fast_result == "fast"
        assert fast_elapsed < 0.15, (
            f"Fast task took {fast_elapsed:.3f}s — event loop may be blocked"
        )

    def test_shutdown_waits_for_all(self, scheduler_class):
        """shutdown() must wait for all tasks to complete."""
        completed: list[str] = []

        async def run():
            scheduler = scheduler_class(max_concurrent=2)

            async def work(name: str) -> str:
                await asyncio.sleep(0.05)
                completed.append(name)
                return name

            for i in range(4):
                asyncio.create_task(scheduler.schedule(f"t{i}", i, work(f"t{i}")))

            await asyncio.sleep(0.01)  # let tasks get scheduled
            await scheduler.shutdown()

        asyncio.run(run())
        assert len(completed) == 4, (
            f"Expected 4 completed tasks after shutdown, got {len(completed)}: {completed}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
