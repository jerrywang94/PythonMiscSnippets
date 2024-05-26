class DisjointSet:

    class DisjointSetMember:
        def __init__(self, value):
            self.value = value
            self.parent = self
            self.rank = 0

    def __init__(self):
        self._members = {}

    def make_set(self, value):
        if value not in self._members:
            self._members[value] = self.DisjointSetMember(value)

        return value

    def find(self, value):
        if value not in self._members:
            raise KeyError("Value not a member of the set!")

        root = self._members.get(value)
        while root.parent != root:
            root = root.parent

        current_node = self._members.get(value)
        while current_node != root:
            parent = current_node.parent
            current_node.parent = root
            current_node = parent

        return root.value

    def union(self, x, y):
        if x not in self._members or y not in self._members:
            raise KeyError("Values not members of the set!")

        x_root = self._members.get(self.find(x))
        y_root = self._members.get(self.find(y))

        if x_root is y_root:
            return

        if x_root.rank < y_root.rank:
            temp = y_root
            y_root = x_root
            x_root = temp

        y_root.parent = x_root
        if x_root.rank == y_root.rank:
            x_root.rank += 1

        return x_root.value
