from src.components.dash_page_progression.tree import DashTree, DashNode
from igraph import Graph


def graph_from(tree: DashTree):
    graph = Graph(directed=True)

    nodes = tree.binary_tree()
    vertices = set()

    root: DashNode = tree.root()

    def build_graph_from(node):
        nonlocal graph, nodes, vertices

        current_regex_symbol = str(node.breadth_first_search_id)

        if current_regex_symbol not in vertices:
            graph.add_vertex(current_regex_symbol)
            vertices |= {current_regex_symbol}

        left_children: DashNode
        right_children: DashNode
        left_children, right_children = nodes[node]

        if left_children:
            left_regex_symbol = str(left_children.breadth_first_search_id)

            graph.add_vertex(left_regex_symbol)
            graph.add_edge(current_regex_symbol, left_regex_symbol)
            build_graph_from(left_children)

        if right_children:
            right_regex_symbol = str(right_children.breadth_first_search_id)

            graph.add_vertex(right_regex_symbol)
            graph.add_edge(current_regex_symbol, right_regex_symbol)
            build_graph_from(right_children)

    build_graph_from(root)

    to_delete_ids = [v.index for v in graph.vs if v.degree() == 0]  # Gathers all vertices without edges and...
    graph.delete_vertices(to_delete_ids)  # Removes them from the graph.

    return graph


if __name__ == '__main__':
    btree = DashTree('aaa#')
    graph_from(btree)
