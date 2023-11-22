import heapq


class Heap:
    """Class implementing a min-heap of tuples (priority, value, index)"""

    def __init__(self):
        self.heap: list[tuple[int, float, int]] = []

    def __str__(self) -> str:
        return str([c for a, b, c in self.heap])

    def left(self, i: int) -> int:
        """
        Returns the index of the left child of the node at index i.

        Parameters:
        - i (int): The index of the node.

        Returns:
        - int: The index of the left child.
        """
        return 2 * i + 1

    def right(self, i: int) -> int:
        """
        Returns the index of the right child of the node at index i.

        Parameters:
        - i (int): The index of the node.

        Returns:
        - int: The index of the right child.
        """
        return 2 * i + 2

    def parent(self, i: int) -> int:
        """
        Returns the index of the parent node for the given index.

        Args:
        - i (int): The index of the node.

        Returns:
        - int: The index of the parent node.
        """
        return (i - 1) // 2

    def min_heapify(self, i: int):
        """
        Rearranges the elements in the heap to maintain the min-heap property.

        Args:
            i (int): Index of the element to start heapify from.
        """
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
        """
        Pushes an item into the heap.

        Args:
        - item (tuple[int, float, int]): The item to be pushed into the heap.
          The tuple should contain three elements: an integer, a float, and an
          integer.
        """
        self.heap.append(item)
        i = len(self.heap) - 1

        while self.parent(i) >= 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)],
                self.heap[i],
            )
            i = self.parent(i)

    def pop(self) -> tuple[int, float, int]:
        """
        Removes and returns the minimum element from the heap.

        Returns:
            A tuple containing the minimum element's attributes: (id, value, priority).
        """
        ret = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
            return ret
        self.heap[0] = self.heap.pop(-1)
        self.min_heapify(0)
        return ret

    def peek(self) -> tuple[int, float, int]:
        """
        Returns the top element of the heap without removing it.

        Returns:
            tuple[int, float, int]: The top element of the heap.
        """
        return self.heap[0]

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return len(self.heap)

    def __iter__(self):
        return iter(self.heap)


# TUI for testing
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
