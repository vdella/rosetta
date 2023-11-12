from src.components.dash_page_progression.tree import DashTree, DashNode
from igraph import Graph


def graph_from(tree: DashTree):
    graph = Graph(directed=True)

    nodes = tree.binary_tree()
    vertices = set()

    root: DashNode = tree.root()

    def build_graph_from(node):
        nonlocal graph, nodes, vertices

        current = str(node.breadth_first_search_id)

        if current not in vertices:
            graph.add_vertex(current)
            vertices |= {current}

        left_children: DashNode
        right_children: DashNode
        left_children, right_children = nodes[node]

        if left_children:
            left = str(left_children.breadth_first_search_id)

            graph.add_vertex(left)
            graph.add_edge(current, left)
            build_graph_from(left_children)

        if right_children:
            right = str(right_children.breadth_first_search_id)

            graph.add_vertex(right)
            graph.add_edge(current, right)
            build_graph_from(right_children)

    build_graph_from(root)

    # Gathers all vertices without edges and...
    to_delete_ids = [v.index for v in graph.vs if v.degree() == 0]

    # Removes them from the graph.
    graph.delete_vertices(to_delete_ids)

    return graph


if __name__ == '__main__':
    btree = DashTree('aaa#')
    graph_from(btree)
