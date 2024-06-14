from typing import Optional

"""
Cartesian tree - values can be anything so long as they are comparable to each other.
Values are extended into a tuple of (value, position in the original array) to accommodate duplicate values.
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


def construct_cartesian_tree(values: list) -> Optional[TreeNode]:
    if not values:
        return None

    curr = None

    for i, v in enumerate(values):
        if curr is None:
            curr = TreeNode((v, i))
            continue

        # Traverse up right side of tree until we either find the root or the node less than the current value
        while (v, i) < curr.value:
            # Smaller than root, set this as the new root
            if curr.parent is None:
                new_root = TreeNode((v, i))
                new_root.left = curr
                curr = new_root
                break

            curr = curr.parent
        else:
            # Parent node doesn't have right child, simply set current as right child
            if curr.right is None:
                curr.right = TreeNode((v, i))
                curr.right.parent = curr
                curr = curr.right
            # Parent node has a right child which we must have traversed through, i.e. the right child is greater
            # than the current candidate node. Make this current node the right child of the parent node, and set
            # the previous right child of the parent node as the left child of this node
            else:
                new_node = TreeNode((v, i))
                new_node.parent = curr

                new_node.left = curr.right
                new_node.left.parent = new_node

                curr.right = new_node
                curr = curr.right

    while curr.parent is not None:
        curr = curr.parent
    return curr
