import plotly.graph_objects as go
from igraph import Layout, Graph
from src.components.dash_page_progression.tree import DashTree
from src.regex.syntax_tree import stringfy


def figure_from(regex):
    tree = DashTree(regex)

    fig = go.Figure()

    Xn, Yn = __build_node_coordinates_for(tree)
    Xe, Ye = __build_edge_coordinates_for(tree)

    __edge_trace_for(fig, Xe, Ye)

    node_annotations = annotations_for(tree)
    mapped_nodes, _ = map_tree_nodes(tree)
    __node_trace_for(fig, Xn, Yn, node_annotations, mapped_nodes)

    fig.update_layout(title_text='Lexical analysis tree',
                      title_x=0.5,
                      font_size=12,
                      showlegend=False,
                      xaxis_visible=False,
                      yaxis_visible=False,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(255,255,255)'
                      )
    return fig


def map_tree_nodes(tree: DashTree):
    reverse_nodes = tree.reverse_level_order_traversal()
    creation_order_nodes = tree.retrieve_serials_by_creation_order()

    combined = list()

    for node in creation_order_nodes.keys():
        reverse, created = reverse_nodes.get(node), creation_order_nodes.get(node)
        combined.append((node, created, reverse))

    return combined


def annotations_for(tree: DashTree) -> list:
    annotations = list()

    def seek_from(node):
        nonlocal annotations

        if node:
            nullable = node.nullable()
            first_pos, last_pos = stringfy(node)

            node_metadata = (node, node.regex_symbol, ('Nullable? {}<br />'
                                                       'first pos: {}<br />'
                                                       'last_pos: {}').format(nullable, first_pos, last_pos))
            annotations.append(node_metadata)

            seek_from(node.left)
            seek_from(node.right)

    seek_from(tree.syntax_tree.root)
    return annotations


def __build_node_coordinates_for(tree: DashTree):
    graphed_tree: Graph = tree.to_graph()
    nr_vertices = len(tree.vertices())

    lay: Layout = graphed_tree.layout_reingold_tilford(root=[str(0)])

    vertices_positions = {k: lay[k] for k in range(nr_vertices)}
    all_target_vertices = [lay[k][1] for k in range(nr_vertices)]
    highest_y_coordinate = max(all_target_vertices)

    L = len(vertices_positions)
    nodes_x_axis = [vertices_positions[k][0] for k in range(L)]
    nodes_y_axis = [2 * highest_y_coordinate - vertices_positions[k][1] for k in range(L)]

    return nodes_x_axis, nodes_y_axis


def __build_edge_coordinates_for(tree: DashTree):
    graphed_tree: Graph = tree.to_graph()
    nr_vertices = len(tree.vertices())

    lay: Layout = graphed_tree.layout_reingold_tilford(root=[str(0)])

    vertices_positions = {k: lay[k] for k in range(nr_vertices)}
    all_target_vertices = [lay[k][1] for k in range(nr_vertices)]
    highest_y_coordinate = max(all_target_vertices)

    edges = [e.tuple for e in graphed_tree.es]

    edges_x_axis = list()
    edges_y_axis = list()

    for edge in edges:
        edges_x_axis += [
            vertices_positions[edge[0]][0],
            vertices_positions[edge[1]][0],
            None]

        edges_y_axis += [
            2 * highest_y_coordinate - vertices_positions[edge[0]][1],
            2 * highest_y_coordinate - vertices_positions[edge[1]][1],
            None]

    return edges_x_axis, edges_y_axis


def __edge_trace_for(figure, Xe, Ye):
    figure.add_trace(go.Scatter(x=Xe,
                                y=Ye,
                                mode='lines',
                                line=dict(color='rgb(210,210,210)', width=1),
                                hoverinfo='none'
                                ))


def __node_trace_for(figure, Xn, Yn, node_annotations: list, mapped_nodes: dict):
    regex_symbols = list()
    nodes_metadata = list()

    for index, node in enumerate(node_annotations):
        _, _, reverse_node_id = mapped_nodes[index]

        _, regex_symbol, metadata = node

        regex_symbols.append(str(reverse_node_id) + ': ' + regex_symbol)
        nodes_metadata.append(metadata)

    figure.add_trace(go.Scatter(x=Xn,
                                y=Yn,
                                mode='markers+text',
                                marker=dict(size=18, opacity=0.4,),
                                text=regex_symbols,
                                customdata=nodes_metadata,
                                hovertemplate="%{customdata}<extra></extra>",
                                hoverinfo='text',
                                opacity=1.0
                                ))


if __name__ == '__main__':
    btree = DashTree('a*#')

    print(map_tree_nodes(btree))

    for n, c, r in map_tree_nodes(btree):
        print(n, c, r)

    print()

    for key, value in btree.reverse_level_order_traversal().items():
        print(key, value)
