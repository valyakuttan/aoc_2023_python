from typing import Generic, TypeVar, Tuple, List
import heapq

T = TypeVar('T')
P = TypeVar('P')


class PriorityQueue(Generic[P, T]):
    def __init__(self):
        self.elements: List[Tuple[P, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: P):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

    def __str__(self) -> str:
        return self.elements.__str__()

if __name__ == '__main__':
    q: PriorityQueue[int, str] = PriorityQueue()
    q.put('a', 5)
    q.put('b', 1)
    q.put('b', 7)
    q.put('b', 2)
    q.get()
    print(q)
