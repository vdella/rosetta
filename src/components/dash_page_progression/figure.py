import plotly.graph_objects as go
from igraph import Layout, Graph
from src.components.dash_page_progression.tree import DashTree
from src.components.dash_page_progression.node import DashNode
from src.components.dash_page_progression.graph import graph_from


def figure_from(regex):
    tree = DashTree(regex)

    fig = go.Figure()

    Xn, Yn = __build_node_coordinates_for(tree)
    Xe, Ye = __build_edge_coordinates_for(tree)

    __edge_trace_for(fig, Xe, Ye)

    dash_nodes = tree.nodes
    __node_trace_for(fig, Xn, Yn, dash_nodes)

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


def __build_node_coordinates_for(tree: DashTree):
    graphed_tree: Graph = graph_from(tree)
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
    graphed_tree: Graph = graph_from(tree)
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


def __node_trace_for(figure, Xn, Yn, node_annotations: dict):
    regex_symbols = list()
    nodes_metadata = list()

    for creation_order_id, dash_node in node_annotations.items():
        dash_node: DashNode

        reverse_node_id = dash_node.reverse_level_creation_id
        regex_symbol = dash_node.regex_symbol

        regex_symbols.append(str(reverse_node_id) + ': ' + regex_symbol)
        nodes_metadata.append(str(dash_node))

    figure.add_trace(go.Scatter(x=Xn,
                                y=Yn,
                                mode='markers+text',
                                marker=dict(size=26, opacity=0.4,),
                                text=regex_symbols,
                                customdata=nodes_metadata,
                                hovertemplate="%{customdata}<extra></extra>",
                                hoverinfo='text',
                                opacity=1.0
                                ))
