from src.regex.syntax_tree import eat, SyntaxTree
from src.components.dash_page_progression.node import DashNode


class DashTree:

    def __init__(self, regex):
        self.regex = regex
        self.syntax_tree = SyntaxTree(self.regex)
        self.nodes: dict = self.dash_nodes()

    def dash_nodes(self):
        nodes = dict()

        reverse_nodes = self.nodes_by_reverse_level_order_traversal()
        creation_order_nodes = self.nodes_by_creation_order()

        def seek_from(node):
            nonlocal nodes

            if node:

                dash_node = DashNode(node)

                dash_node.reverse_level_creation_id = reverse_nodes[node]
                creation_order_id = creation_order_nodes[node]

                nodes[creation_order_id] = dash_node

                seek_from(node.left)
                seek_from(node.right)

        seek_from(self.syntax_tree.root)
        return dict(sorted(nodes.items()))

    def nodes_by_creation_order(self):
        nodes_by_ids = dict()

        root = self.syntax_tree.root
        serial = 0

        def gather_from(node):
            nonlocal nodes_by_ids, serial

            if node not in nodes_by_ids:
                nodes_by_ids[node] = serial
                serial += 1

            left, right = node.left, node.right

            if left:
                gather_from(left)
            if right:
                gather_from(right)

        gather_from(root)

        return nodes_by_ids

    def nodes_by_reverse_level_order_traversal(self):
        if not self.syntax_tree.root:
            return []

        syntax_tree = self.syntax_tree

        serial = len(self.vertices())
        queue = [(syntax_tree.root, serial)]
        stack = []
        traversal = []

        while queue:
            current, serial = queue.pop(0)
            stack.append((current, serial))

            if current.right:
                serial -= 1
                queue.append((current.right, serial))
            if current.left:
                serial -= 1
                queue.append((current.left, serial))

        while stack:
            traversal.append(stack.pop())

        return dict(traversal)

    def vertices(self) -> list:
        nodes, _ = eat(self.regex)

        # Parenthesis should not be counted as tree nodes.
        parenthesis = {'(', ')'}
        nodes = [e for e in nodes if e not in parenthesis]

        return nodes


if __name__ == '__main__':
    tree = DashTree('aaa#')

    for k, v in tree.nodes.items():
        print(k, v)
