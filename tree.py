from typing import Optional
from heap import Heap
import graphviz
from enum import Enum
import os

# class syntax


class Color(Enum):
    RED = 1
    BLACK = 2


class NodeData:
    def __init__(
        self, book_id: int, book_name: str, author_name: str, is_available: bool
    ) -> None:
        self.book_id: int = book_id
        self.book_name: str = book_name
        self.author_name: str = author_name
        self.is_available: bool = is_available
        self.borrowed_by: int | None = None
        self.reservation_heap: Heap = Heap()

    def __str__(self) -> str:
        ret = []
        ret.append(f"BookID = {self.book_id}")
        ret.append(f'Title = "{self.book_name}"')
        ret.append(f'Author = "{self.author_name}"')
        if self.is_available:
            ret.append('Availability = "Yes"')
        else:
            ret.append('Availability = "No"')
        ret.append(f"BorrowedBy = {self.borrowed_by}")
        ret.append(f"Reservations = {self.reservation_heap.__str__()}")

        return "\n".join(ret)


class TreeNode:
    def __init__(self, key: int, data, color: Color) -> None:
        self.left: "TreeNode" | None = None
        self.right: "TreeNode" | None = None
        self.key: int = key
        self.data: NodeData = data
        self.color: Color = color
        self.p: "TreeNode" | None = None


class Tree:
    def __init__(self) -> None:
        self.root_node: TreeNode | None = None
        self.sentinel = TreeNode(-1, None, Color.BLACK)
        self.flip_count = 0

    def left_rotate(self, x: TreeNode):
        y = x.right
        if y is self.sentinel:
            return x
        assert y is not None

        beta = y.left
        if beta is not self.sentinel:
            assert beta is not None
            beta.p = x
            x.right = beta
        else:
            x.right = self.sentinel

        if x.p is None:  # x is the root node
            self.root_node = y
        elif x.p.left == x:  # x is left child
            x.p.left = y
        elif x.p.right == x:  # x is right child
            x.p.right = y
        else:
            raise Exception("Something went wrong")

        y.p = x.p
        x.p = y
        y.left = x

    def right_rotate(self, y: TreeNode):
        x = y.left
        if x is self.sentinel:
            return y
        assert x is not None

        beta = x.right
        if beta is not self.sentinel:
            assert beta is not None
            beta.p = y
            y.left = beta
        else:
            y.left = self.sentinel

        if y.p is None:  # y is the root node
            self.root_node = x
        elif y.p.left == y:  # y is left child
            y.p.left = x
        elif y.p.right == y:  # y is right child
            y.p.right = x
        else:
            raise Exception("Something went wrong")

        x.p = y.p
        y.p = x
        x.right = y

    def insert(self, key: int, value: None | NodeData) -> TreeNode:
        # binary search
        parent: None | TreeNode = None
        current: None | TreeNode = self.root_node

        while current and current is not self.sentinel:
            parent = current
            if current.key > key:
                current = current.left
            elif current.key < key:
                current = current.right
            else:
                return current

        new_node = TreeNode(key, value, Color.RED)
        new_node.left = self.sentinel
        new_node.right = self.sentinel
        if parent:
            new_node.p = parent
        if not parent:
            self.root_node = new_node
        elif parent.key < key:
            parent.right = new_node
        elif parent.key > key:
            parent.left = new_node

        # fix the tree to satisfy red-black tree properties
        self._insert_fixup(new_node)

        return new_node

    def _insert_fixup(self, node: TreeNode) -> None:
        while node.p and node.p.color == Color.RED:
            if node.p == node.p.p.left:
                y = node.p.p.right  # uncle
                if y.color == Color.RED:
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(y, Color.BLACK)
                    self._flip_color(node.p.p, Color.RED)
                    assert node.p.p
                    node = node.p.p
                else:
                    if node == node.p.right:
                        node = node.p
                        self.left_rotate(node)
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(node.p.p, Color.RED)
                    self.right_rotate(node.p.p)
            else:
                y = node.p.p.left
                if y.color == Color.RED:
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(y, Color.BLACK)
                    self._flip_color(node.p.p, Color.RED)
                    assert node.p.p
                    node = node.p.p
                else:
                    if node == node.p.left:
                        node = node.p
                        self.right_rotate(node)
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(node.p.p, Color.RED)
                    self.left_rotate(node.p.p)

        assert self.root_node is not None
        self.root_node.color = Color.BLACK

    def transplant(self, u: TreeNode, v: TreeNode) -> None:
        """Replaces subtree rooted at u with subtree rooted at v"""
        # assert u.p is not None
        # assert v.p is not None
        if u.p is None or u.p is self.sentinel:
            self.root_node = v
        elif u == u.p.left:
            u.p.left = v
        elif u == u.p.right:
            u.p.right = v

        v.p = u.p

    def _flip_color(self, node: TreeNode, color: Color) -> None:
        assert type(node) == TreeNode
        if not node or node is self.sentinel or node.color == color:
            return
        node.color = color
        self.flip_count += 1

    def delete(self, key):
        node: TreeNode | None = self.search(key)
        assert node is not None
        assert node.left is not None
        assert node.right is not None

        y = node
        y_original_color = y.color

        if node.left == self.sentinel:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.sentinel:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right

            if y.p != node:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.p = y
            else:
                x.p = y

            self.transplant(node, y)
            y.left = node.left
            y.left.p = y
            self._flip_color(y, node.color)

        if y_original_color == Color.BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, node: TreeNode):
        while node != self.root_node and node.color == Color.BLACK:
            assert node.p
            assert node.p.left
            assert node.p.right

            if node == node.p.left:
                w: TreeNode = node.p.right  # sibling

                if w.color == Color.RED:
                    self._flip_color(w, Color.BLACK)
                    self._flip_color(node.p, Color.RED)
                    self.left_rotate(node.p)
                    w = node.p.right

                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    self._flip_color(w, Color.RED)
                    node = node.p
                else:
                    if w.right.color == Color.BLACK:
                        self._flip_color(w.left, Color.BLACK)
                        self._flip_color(w, Color.RED)
                        self.right_rotate(w)
                        w = node.p.right

                    self._flip_color(w, node.p.color)
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(w.right, Color.BLACK)
                    self.left_rotate(node.p)
                    node = self.root_node
            else:
                w = node.p.left

                if w.color == Color.RED:
                    self._flip_color(w, Color.BLACK)
                    self._flip_color(node.p, Color.RED)
                    self.right_rotate(node.p)
                    w = node.p.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    self._flip_color(w, Color.RED)
                    node = node.p
                else:
                    if w.left.color == Color.BLACK:
                        self._flip_color(w.right, Color.BLACK)
                        self._flip_color(w, Color.RED)
                        self.left_rotate(w)
                        w = node.p.left

                    self._flip_color(w, node.p.color)
                    self._flip_color(node.p, Color.BLACK)
                    self._flip_color(w.left, Color.BLACK)
                    self.right_rotate(node.p)
                    node = self.root_node

        self._flip_color(node, Color.BLACK)

    def search(self, key: int) -> TreeNode | None:
        node = self.root_node
        while node is not self.sentinel:
            assert node is not None
            if node.key == key:
                return node
            elif node.key < key:
                node = node.right
            else:
                node = node.left

        return None

    def _minimum(self, node: TreeNode) -> TreeNode:
        while node.left is not self.sentinel:
            assert node.left is not None
            node = node.left

        return node

    def find_closest(self, key: int) -> list[TreeNode]:
        def find_lesser(node) -> TreeNode | None:
            ans = None
            while node and node is not self.sentinel:
                if node.key == key:
                    return node
                elif node.key < key:
                    ans = node
                    node = node.right
                else:
                    node = node.left

            return ans

        def find_greater(node) -> TreeNode | None:
            ans = None
            while node and node is not self.sentinel:
                if node.key == key:
                    return node
                elif node.key > key:
                    ans = node
                    node = node.left
                else:
                    node = node.right

            return ans

        lesser = find_lesser(self.root_node)
        greater = find_greater(self.root_node)

        assert lesser is not self.sentinel
        assert greater is not self.sentinel

        if lesser is None and greater is None:
            return []
        elif lesser is None:
            return [greater]
        elif greater is None:
            return [lesser]
        elif key - lesser.key < greater.key - key:
            return [lesser]
        elif key - lesser.key > greater.key - key:
            return [greater]
        elif lesser.key == greater.key:
            return [lesser]
        else:
            return [lesser, greater]

    def range_search(self, start: int, end: int) -> list[TreeNode]:
        """Returns a list of nodes whose keys are in the range [start, end]
        (inclusive)"""

        def helper(node) -> list[TreeNode]:
            if node is self.sentinel:
                return []
            elif node.key < start:
                return helper(node.right)
            elif node.key > end:
                return helper(node.left)
            else:
                return helper(node.left) + [node] + helper(node.right)

        return helper(self.root_node)

    def visualize_binary_tree(self, file_name):
        counter = 0
        dot = graphviz.Digraph(
            graph_attr={"label": f"Color flip count: {self.flip_count}"}
        )
        if not self.root_node:
            return
        dot.node(str(self.root_node.key))

        def add_nodes_edges(node):
            if node is not self.sentinel:
                color = "red" if node.color == Color.RED else "black"
                dot.node(
                    str(node.key),
                    _attributes={
                        "shape": "circle",
                        "color": color,
                        "penwidth": "3",
                    },
                )

            if not node.left and not node.right:
                return

            nonlocal counter
            if node.left is not self.sentinel:
                dot.edge(str(node.key), str(node.left.key))
                add_nodes_edges(node.left)
            elif node.left is self.sentinel:
                counter += 1
                dot.node("stn " + str(counter), _attributes={"shape": "box"})
                dot.edge(
                    str(node.key),
                    "stn " + str(counter),
                    _attributes={"style": "dashed"},
                )
            if node.right is not self.sentinel:
                dot.edge(str(node.key), str(node.right.key))
                add_nodes_edges(node.right)
            elif node.right is self.sentinel:
                counter += 1
                dot.node("stn " + str(counter), _attributes={"shape": "box"})
                dot.edge(
                    str(node.key),
                    "stn " + str(counter),
                    _attributes={"style": "dashed"},
                )
            if node.p:
                dot.edge(
                    str(node.key), str(node.p.key), _attributes={"style": "dashed"}
                )

        add_nodes_edges(self.root_node)
        dot.render(file_name, view=False, format="png")


if __name__ == "__main__":
    tree = Tree()

    while True:
        print(f"Color flip count:", tree.flip_count)
        command = input("Enter command: ")
        tree.visualize_binary_tree("before")
        if command.startswith("insert"):
            value = int(command.split(" ")[-1])
            tree.insert(value, None)
        elif command.startswith("delete"):
            value = int(command.split(" ")[-1])
            tree.delete(value)

        tree.visualize_binary_tree("after")
