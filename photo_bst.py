from binary_tree import AVLTree
from photo import Photo

class PhotoBST(AVLTree):
    def __init__(self):
        super().__init__()

    def delete(self, value):
        existe, _ = self.search(value)
        if existe:
            super().delete(value)
            self._qtd_nodes -= 1

    def successor(self, node):
        if not node:
            return None
        if node.right_node():
            return self.minimum(node.right_node())

        parent = node.parent_node()
        current = node
        while parent and current == parent.right_node():
            current = parent
            parent = parent.parent_node()
        return parent

    def predecessor(self, node):
        if not node:
            return None
        if node.left_node():
            return self.maximum(node.left_node())

        parent = node.parent_node()
        current = node
        while parent and current == parent.left_node():
            current = parent
            parent = parent.parent_node()
        return parent

    def range(self, ts1: int, ts2: int):
        result = []
        self._range_recursive(self._root, ts1, ts2, result)
        return result

    def _range_recursive(self, node, ts1, ts2, result):
        if not node or node.empty():
            return

        photo = node.data()

        if photo.ts >= ts1:
            self._range_recursive(node.left_node(), ts1, ts2, result)

        if ts1 <= photo.ts <= ts2:
            result.append(photo)

        if photo.ts <= ts2:
            self._range_recursive(node.right_node(), ts1, ts2, result)

    def nearest(self, ts: int):
        if self.empty():
            return None

        closest = None
        min_diff = float('inf')
        current = self._root

        while current and not current.empty():
            photo = current.data()
            diff = abs(photo.ts - ts)

            if diff < min_diff or (diff == min_diff and (closest is None or photo.id < closest.id)):
                min_diff = diff
                closest = photo

            if ts < photo.ts:
                current = current.left_node()
            elif ts > photo.ts:
                current = current.right_node()
            else:
                break 

        return closest