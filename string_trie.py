# String Trie
class StringTrie:
    def __init__(self):
        self.root = StringTrie.Node()

    class Node:
        def __init__(self, parent: 'StringTrie.Node' = None):
            self.parent = parent
            self.children = {}
            self.terminal = False

    def insert(self, s: str):
        if not s:
            return
        curr = self.root
        for c in s:
            curr = curr.children.setdefault(c, StringTrie.Node(parent=curr))
        curr.terminal = True

    def find(self, s: str) -> bool:
        curr = self.root
        for c in s:
            if c not in curr.children:
                return False
            curr = curr.children[c]

        if not curr.terminal:
            return False

        return True

    def delete(self, s: str):
        curr = self.root
        for c in s:
            if c not in curr.children:
                return
            curr = curr.children[c]

        curr.terminal = False
        if curr.children:
            return
        curr = curr.parent

        for c in reversed(s):
            del curr.children[c]
            if curr.children:
                return
            curr = curr.parent
