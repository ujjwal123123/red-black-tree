from typing import Optional
import graphviz
from enum import Enum


class Color(Enum):
    """
    Enum representing the color of a node in a tree.
    """

    RED = 1
    BLACK = 2


class TreeNode:
    """
    Represents a node in a binary tree.

    Attributes:
        key (int): The key value of the node.
        data: The data stored in the node.
        color (Color): The color of the node.
        left (TreeNode): The left child of the node.
        right (TreeNode): The right child of the node.
        p (TreeNode | None): The parent of the node.
    """

    def __init__(self, key: int, data, color: Color) -> None:
        self.left: "TreeNode"
        self.right: "TreeNode"
        self.key: int = key
        self.data = data
        self.color: Color = color
        self.p: "TreeNode" | None = None


class SentinelNode(TreeNode):
    def __init__(self) -> None:
        super().__init__(-1, None, Color.BLACK)


class Tree:
    def __init__(self) -> None:
        self.sentinel = SentinelNode()
        self.root_node: TreeNode = self.sentinel
        self.flip_count = 0

    def get_colors(self) -> dict[int, Color]:
        """
        Returns a dictionary mapping each node's key to its color.

        Returns:
            dict[int, Color]: A dictionary where the keys are node keys and the values are node colors.
        """
        ret = {}

        def helper(node: TreeNode):
            if node is None or node is self.sentinel:
                return
            ret[node.key] = node.color
            helper(node.left)
            helper(node.right)

        helper(self.root_node)

        return ret

    def update_color_flips(
        self, before: dict[int, Color], after: dict[int, Color]
    ) -> int:
        ans = 0
        for key in before.keys():
            if key in after.keys() and before[key] != after[key]:
                ans += 1
        self.flip_count += ans
        return ans

    def left_rotate(self, x: TreeNode):
        """
        Left rotates the given node in the binary tree.

        Args:
            x (TreeNode): The node to be left rotated.

        """
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

    def insert(self, key: int, value) -> TreeNode:
        colors_before = self.get_colors()
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

        colors_after = self.get_colors()
        self.update_color_flips(colors_before, colors_after)

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
        if u.p is None or u.p is self.sentinel:
            self.root_node = v
        elif u == u.p.left:
            u.p.left = v
        elif u == u.p.right:
            u.p.right = v

        v.p = u.p

    def _flip_color(self, node: TreeNode, color: Color) -> None:
        if not node or node is self.sentinel or node.color == color:
            return
        node.color = color

    def delete(self, key):
        colors_before = self.get_colors()
        z: TreeNode | None = self.search(key)
        assert z and z is not self.sentinel

        y = z
        y_original_color = y.color

        if z.left is self.sentinel:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is self.sentinel:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y != z.right:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            else:
                x.p = y

            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            self._flip_color(y, z.color)

        if y_original_color == Color.BLACK:
            self._delete_fixup(x)

        colors_after = self.get_colors()
        self.update_color_flips(colors_before, colors_after)

    def _delete_fixup(self, node: TreeNode):
        while node != self.root_node and node.color == Color.BLACK:
            assert node.p

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

    def search(self, key: int) -> TreeNode:
        node = self.root_node
        while node is not self.sentinel:
            if node.key == key:
                return node
            elif node.key < key:
                node = node.right
            else:
                node = node.left

        return node

    def _minimum(self, node: TreeNode) -> TreeNode:
        while node.left is not self.sentinel:
            node = node.left
        return node

    def find_closest(self, key: int) -> list[TreeNode]:
        def find_lesser(node: TreeNode) -> TreeNode:
            ans = self.sentinel
            while node and node is not self.sentinel:
                if node.key == key:
                    return node
                elif node.key < key:
                    ans = node
                    node = node.right
                else:
                    node = node.left

            return ans

        def find_greater(node: TreeNode) -> TreeNode:
            ans = self.sentinel
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

        if lesser is self.sentinel and greater is self.sentinel:
            return []
        elif lesser is self.sentinel:
            return [greater]
        elif greater is self.sentinel:
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

            if node is self.sentinel or (not node.left and not node.right):
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
