from collections import deque
from typing import TypeVar, Generic

T = TypeVar('T')

class Queue(Generic[T]):
    def __init__(self):
        self.elements: deque[T] = deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()
