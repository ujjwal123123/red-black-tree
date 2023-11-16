from typing import Optional
from heap import Heap
import graphviz
from enum import Enum

# class syntax


class Color(Enum):
    RED = 1
    BLACK = 2


class NodeData:
    book_name: str
    author_name: str
    availability_status: bool
    borrowed_by: str
    reservation_heap: Heap = Heap()


class TreeNode:
    def __init__(self, key: int, data, color: Color | None = None) -> None:
        self.left: "TreeNode" | None = None
        self.right: "TreeNode" | None = None
        self.key: int = key
        self.data: NodeData | None = data
        self.color: Color | None = color
        self.p: "TreeNode" | None = None


# sentinel = TreeNode(None, None)


class Tree:
    def __init__(self) -> None:
        self.root_node: TreeNode | None = None
        self.sentinel = TreeNode(-1, None, Color.BLACK)

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
                    node.p.color = Color.BLACK
                    y.color = Color.BLACK
                    node.p.p.color = Color.RED
                    node = node.p.p
                else:
                    if node == node.p.right:
                        node = node.p
                        self.left_rotate(node)
                    node.p.color = Color.BLACK
                    node.p.p.color = Color.RED
                    self.right_rotate(node.p.p)
            else:
                y = node.p.p.left
                if y.color == Color.RED:
                    node.p.color = Color.BLACK
                    y.color = Color.BLACK
                    node.p.p.color = Color.RED
                    node = node.p.p
                else:
                    if node == node.p.left:
                        node = node.p
                        self.right_rotate(node)
                    node.p.color = Color.BLACK
                    node.p.p.color = Color.RED
                    self.left_rotate(node.p.p)

        self.root_node.color = Color.BLACK

    def visualize_binary_tree(self, file_name):
        counter = 0
        dot = graphviz.Digraph()
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


tree = Tree()
node1 = tree.insert(1, None)
tree.visualize_binary_tree("before")
input()
node3 = tree.insert(3, None)
tree.visualize_binary_tree("before")
input()
node4 = tree.insert(4, None)
tree.visualize_binary_tree("before")
input()
node2 = tree.insert(2, None)
tree.visualize_binary_tree("before")
input()
node0 = tree.insert(0, None)
tree.visualize_binary_tree("before")
input()
node0 = tree.insert(5, None)
tree.visualize_binary_tree("before")
input()
node0 = tree.insert(6, None)
tree.visualize_binary_tree("before")
input()
node0 = tree.insert(7, None)
tree.visualize_binary_tree("before")
input()
# # tree.left_rotate(node3)
# tree.visualize_binary_tree("after")
# # tree.right_rotate(node4)
# tree.visualize_binary_tree("after_right")
