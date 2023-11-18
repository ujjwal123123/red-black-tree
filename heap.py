import heapq


class Heap:
    def __init__(self):
        self.heap: list[tuple[int, float, int]] = []

    def __str__(self) -> str:
        return str([c for a, b, c in self.heap])

    def push(self, item: tuple[int, float, int]):
        heapq.heappush(self.heap, item)

    def pop(self) -> tuple[int, float, int]:
        return heapq.heappop(self.heap)

    def peek(self) -> tuple[int, float, int]:
        return self.heap[0]

    def __len__(self):
        return len(self.heap)

    def __iter__(self):
        return iter(self.heap)
