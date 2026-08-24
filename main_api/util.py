__all__ = [
    "define_task",
]

from types import CoroutineType
from typing import Callable, TypeVar

from taskiq import AsyncTaskiqDecoratedTask

T = TypeVar("T")


def define_task(
    task: AsyncTaskiqDecoratedTask[..., CoroutineType[object, object, T]],
):
    def wrapper(func: Callable[..., CoroutineType[object, object, T]]):
        new_task = task.broker.register_task(func, task.task_name)
        return new_task

    return wrapper
