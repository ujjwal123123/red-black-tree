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
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.key: int = key
        self.data: None | NodeData = data
        self.color: Color | None = color
        self.p = None


# sentinel = TreeNode(None, None)


class Tree:
    def __init__(self) -> None:
        self.root_node: TreeNode | None = None
        self.sentinel = TreeNode(-1, None, Color.BLACK)

    def insert(self, key: int, value: None | NodeData) -> TreeNode:
        # binary search
        parent: None | TreeNode = None
        current: None | TreeNode = self.root_node

        while current:
            parent = current
            if current.key > key:
                current = current.left
            elif current.key < key:
                current = current.right
            else:
                return current

        new_node = TreeNode(key, value)
        if not parent:
            self.root_node = new_node
        elif parent.key < key:
            parent.right = new_node
        elif parent.key > key:
            parent.left = new_node
        return new_node

    def visualize_binary_tree(self):
        dot = graphviz.Digraph()
        dot.node(str(self.root_node.key))

        def add_nodes_edges(node):
            if node.left:
                dot.node(str(node.left.key))
                dot.edge(str(node.key), str(node.left.key))
                add_nodes_edges(node.left)
            if node.right:
                dot.node(str(node.right.key))
                dot.edge(str(node.key), str(node.right.key))
                add_nodes_edges(node.right)

        add_nodes_edges(self.root_node)
        dot.render("binary_tree", view=False, format="png")


tree = Tree()
tree.insert(1, None)
tree.insert(2, None)
tree.insert(3, None)
tree.insert(0, None)

tree.visualize_binary_tree()
