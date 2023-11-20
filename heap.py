import heapq


class Heap:
    """Class implementing a min-heap of tuples (priority, value, index)"""

    def __init__(self):
        self.heap: list[tuple[int, float, int]] = []

    def __str__(self) -> str:
        return str([c for a, b, c in self.heap])

    def left(self, i: int) -> int:
        return 2 * i + 1

    def right(self, i: int) -> int:
        return 2 * i + 2

    def parent(self, i: int) -> int:
        return (i - 1) // 2

    def min_heapify(self, i: int):
        left = self.left(i)
        right = self.right(i)

        largest = i
        if left < len(self.heap) and self.heap[left] < self.heap[i]:
            largest = left
        if right < len(self.heap) and self.heap[right] < self.heap[largest]:
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.min_heapify(largest)

    def push(self, item: tuple[int, float, int]):
        self.heap.append(item)
        i = len(self.heap) - 1

        while self.parent(i) >= 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)],
                self.heap[i],
            )
            i = self.parent(i)

    def pop(self) -> tuple[int, float, int]:
        ret = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
            return ret
        self.heap[0] = self.heap.pop(-1)
        self.min_heapify(0)
        return ret

    def peek(self) -> tuple[int, float, int]:
        return self.heap[0]

    def __len__(self):
        return len(self.heap)

    def __iter__(self):
        return iter(self.heap)


if __name__ == "__main__":
    heap = Heap()
    while True:
        command = input("Enter command: ")
        if command.startswith("push"):
            key = int(command.split()[-1])
            heap.push((key, 0, 0))
        elif command.startswith("pop"):
            print(heap.pop())

        print(heap)
