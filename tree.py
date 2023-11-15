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

        new_node = TreeNode(key, value)
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
        return new_node

    def visualize_binary_tree(self, file_name):
        counter = 0
        dot = graphviz.Digraph()
        dot.node(str(self.root_node.key))

        def add_nodes_edges(node):
            nonlocal counter
            if node.left is not self.sentinel:
                dot.node(str(node.left.key))
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
                dot.node(str(node.right.key))
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
node = tree.insert(1, None)
tree.insert(3, None)
tree.insert(4, None)
tree.insert(2, None)
tree.insert(0, None)
tree.visualize_binary_tree("before")
tree.left_rotate(node)

tree.visualize_binary_tree("after")
