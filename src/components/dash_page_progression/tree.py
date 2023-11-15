from src.regex.syntax_tree import eat, SyntaxTree
from src.components.dash_page_progression.node import DashNode
from collections import OrderedDict


class DashTree:

    def __init__(self, regex):
        self.regex = regex
        self.syntax_tree = SyntaxTree(self.regex)
        self.nodes: dict = self.dash_nodes()

    def dash_nodes(self):
        nodes = dict()

        reverse_nodes = self.nodes_by_reverse_level_order_traversal()
        creation_order_nodes = self.nodes_by_creation_order()
        breadth_first_search_ids = self.nodes_by_bfs_order()

        def seek_from(node):
            nonlocal nodes

            if node:

                dash_node = DashNode(node)

                dash_node.reverse_level_creation_id = reverse_nodes[node]
                dash_node.breadth_first_search_id = breadth_first_search_ids[node]

                creation_order_id = creation_order_nodes[node]

                nodes[creation_order_id] = dash_node

                seek_from(node.left)
                seek_from(node.right)

        seek_from(self.syntax_tree.root)
        return dict(sorted(nodes.items()))

    def find(self, node):
        if node:

            for current in self.nodes.values():
                current: DashNode

                if current.syntax_tree_node == node:
                    return current

        return None

    def root(self):
        return self.find(self.syntax_tree.root)

    def binary_tree(self) -> dict:
        binary_tree = OrderedDict()

        syntax_tree_root = self.syntax_tree.root
        root = self.find(syntax_tree_root)

        def build_from(node):
            nonlocal binary_tree

            left, right = self.find(node.syntax_tree_node.left), self.find(node.syntax_tree_node.right)
            binary_tree[node] = (left, right)

            if left:
                build_from(left)

            if right:
                build_from(right)

        build_from(root)
        return dict(binary_tree)

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

        queue = [syntax_tree.root]
        stack = []
        traversal = []

        # Traverse the tree and store nodes in stack
        while queue:
            current = queue.pop(0)
            stack.append(current)

            # Add children to the queue
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        # Assign serial numbers in reverse order
        serial = 1
        while stack:
            current = stack.pop()
            traversal.append((current, serial))
            serial += 1

        return dict(traversal)

    def nodes_by_bfs_order(self):
        if not self.syntax_tree.root:
            return []

        syntax_tree = self.syntax_tree

        serial = 0
        to_be_visited_queue = [syntax_tree.root]

        nodes_by_ids = {syntax_tree.root: serial}

        while to_be_visited_queue:
            current = to_be_visited_queue.pop(0)

            if current.left:
                to_be_visited_queue.append(current.left)
                serial += 1
                nodes_by_ids[current.left] = serial

            if current.right:
                to_be_visited_queue.append(current.right)
                serial += 1
                nodes_by_ids[current.right] = serial

        return nodes_by_ids

    def vertices(self) -> list:
        nodes, _ = eat(self.regex)

        # Parenthesis should not be counted as tree nodes.
        parenthesis = {'(', ')'}
        nodes = [e for e in nodes if e not in parenthesis]

        return nodes


if __name__ == '__main__':
    tree = DashTree('(0|1)*1(0|1)(0|1)(0|1)(0|1)(0|1)#')

    print(len(tree.vertices()))

    for k, v in tree.nodes_by_reverse_level_order_traversal().items():
        print(k, v)
