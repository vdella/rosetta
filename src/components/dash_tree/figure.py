import plotly.graph_objects as go
from igraph import Layout, Graph
from src.components.dash_tree.tree import DashTree


def __build_node_coordinates_for(tree: DashTree):
    graphed_tree: Graph = tree.to_graph()
    _, nr_vertices = tree.vertices()

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
    _, nr_vertices = tree.vertices()

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


def __node_trace_for(figure, Xn, Yn):
    figure.add_trace(go.Scatter(x=Xn,
                                y=Yn,
                                mode='markers',
                                name='bla',
                                marker=dict(symbol='circle-dot',
                                            size=18,
                                            color='#6175c1',  # '#DB4551',
                                            line=dict(color='rgb(50,50,50)', width=1)
                                            ),
                                customdata=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                hovertemplate="%{customdata}<extra></extra>",
                                hoverinfo='text',
                                opacity=0.8
                                ))


def figure_from(regex):
    tree = DashTree(regex)

    fig = go.Figure()

    Xn, Yn = __build_node_coordinates_for(tree)
    Xe, Ye = __build_edge_coordinates_for(tree)

    __edge_trace_for(fig, Xe, Ye)

    __node_trace_for(fig, Xn, Yn)

    fig.update_layout(title_text='Lexical analysis tree',
                      title_x=0.5,
                      font_size=12,
                      showlegend=False,
                      xaxis_visible=False,
                      yaxis_visible=False,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    return fig


if __name__ == '__main__':
    f = figure_from('(ab)*ab')
    f.show()
