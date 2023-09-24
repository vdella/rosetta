from igraph import Graph
from src.regex.syntax_tree import eat, SyntaxTree, stringfy


class DashTree:

    def __init__(self, regex):
        self.regex = regex
        self.syntax_tree = SyntaxTree(self.regex)

    def to_graph(self):
        graph = Graph(directed=True)

        nodes = self.map_linked_nodes_to_ids()
        vertices = set()

        root = 0
        vertices |= {str(root)}
        graph.add_vertex(str(root))

        def build_graph_from(node):
            nonlocal graph, nodes, vertices

            if node not in vertices:
                graph.add_vertex(str(node))
                vertices |= {str(node)}

            _, left_children, right_children = nodes[node]

            if left_children:
                graph.add_vertex(str(left_children))
                graph.add_edge(str(node), str(left_children))
                build_graph_from(left_children)

            if right_children:
                graph.add_vertex(str(right_children))
                graph.add_edge(str(node), str(right_children))
                build_graph_from(right_children)

        build_graph_from(root)

        to_delete_ids = [v.index for v in graph.vs if v.degree() == 0]  # Gathers all vertices without edges and...
        graph.delete_vertices(to_delete_ids)  # Remove them from the graph.

        return graph

    def map_linked_nodes_to_ids(self):
        enumerated_nodes = self.enumerated_nodes()
        linked_nodes = self.linked_nodes()

        linked_numbered_nodes = dict()

        for node in linked_nodes.items():
            key = node[0]
            level, left_children, right_children = node[1][0], node[1][1], node[1][2]  # Disassembles tuple values.

            key = enumerated_nodes[key]  # Will never be None. Hence, we do not verify.

            if enumerated_nodes.get(left_children):
                left_children = enumerated_nodes[left_children]

            if enumerated_nodes.get(right_children):
                right_children = enumerated_nodes[right_children]

            linked_numbered_nodes[key] = (level, left_children, right_children)

        return linked_numbered_nodes

    def enumerated_nodes(self):
        """Does a breadth-first search from the tree root
        in order to map every node to a single exclusive integer.
        With every node having an int id, handling the graph build
        is easier as an igraph uses int labeled nodes. Their str description
        shall be added later during execution as their labels."""
        enumerated_nodes = dict()

        point = self.syntax_tree.root

        to_visit = [point]
        enumerated_nodes[point] = 0

        graph_id = 0

        while to_visit:
            point = to_visit.pop(0)

            if point:
                enumerated_nodes[point] = graph_id
                graph_id += 1

                to_visit.append(point.left)
                to_visit.append(point.right)

        return enumerated_nodes

    def linked_nodes(self):
        """Does a breadth-first search in order to
        fully build the binary tree lexical tree. Every parent
        works as a dict key, with their respective values being
        associated with their (tree height (top-down), left and right
        children)."""
        linked_nodes = dict()

        point = self.syntax_tree.root

        to_visit = [(0, point)]

        while to_visit:
            level, point = to_visit.pop(0)

            if point:
                linked_nodes[point] = (level, point.left, point.right)

                to_visit.append((level + 1, point.left))
                to_visit.append((level + 1, point.right))

        return linked_nodes

    def vertices(self) -> list and int:
        """From a regex, finds the node count by finding missing concatenations and the hashtag."""
        nodes, _ = eat(self.regex)

        # Parenthesis should not be counted as tree nodes.
        parenthesis = {'(', ')'}
        nodes = [e for e in nodes if e not in parenthesis]

        return nodes, len(nodes)

    def node_annotations(self) -> dict:
        annotations = dict()

        def seek_from(node):
            nonlocal annotations

            if node:
                nullable = node.nullable()
                first_pos, last_pos = stringfy(node)

                annotations[node] = ('Nullable? {}/n'
                                     'first pos: {}/n '
                                     'last_pos: {}').format(nullable, first_pos, last_pos)

                seek_from(node.left)
                seek_from(node.right)

        seek_from(self.syntax_tree.root)
        return annotations
