from dash import Dash, html, dcc, Input, Output, callback
from src.components.dash_page_progression.page import DashPage
from src.components.dash_page_progression.figure import map_tree_nodes, annotations_for
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure

page = DashPage.empty_dash_page()

regex_symbols = set()
nodes_metadata = list()

mapped_nodes = dict()
node_annotations = list()

external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.Br(),

        html.H1(children='Rosetta', style={'textAlign': 'center'}),

        html.Br(),
        html.Br(),

        html.Div(
            children=[
                dcc.Input(
                    id='regex-input',
                    placeholder='Type your favorite regex!',
                    debounce=True),
            ],
            style={'textAlign': 'center'},
        ),

        html.Br(),

        html.Div(
            children=[
                dbc.Button('Submit', id='submit-button'),
            ],
            style={'textAlign': 'center'}),

        html.Br(),
        html.Br(),

        html.Div(
            id='figure-parent',
            children=[
                dcc.Graph(
                    id='bin-tree',
                    figure={},
                ),
            ],
            hidden=True,
        ),

        html.Div(
            id='tree-page-handler',
            children=[
                dbc.Pagination(
                    id='pagination',
                    max_value=0,
                    first_last=True,
                    previous_next=True,
                    fully_expanded=False),
            ],
            style={'textAlign': 'center'},
            hidden=True
        ),

        html.Br(),
    ]))


@callback(
    Output('figure-parent', 'hidden'),
    Output('tree-page-handler', 'hidden'),
    Output('pagination', 'max_value'),
    Output('bin-tree', 'figure', allow_duplicate=True),
    Input('regex-input', 'value'),
    prevent_initial_call=True)
def create_figure_from(user_text_entry):
    hidden_figure, hidden_page_handler = True, True

    if user_text_entry:
        global page
        page = DashPage(user_text_entry)

        global mapped_nodes
        mapped_nodes = map_tree_nodes(page.finalized_tree)

        global node_annotations
        node_annotations = annotations_for(page.finalized_tree)

        return not hidden_figure, not hidden_page_handler, page.page_quantity(), page.final_figure
    return hidden_figure, hidden_page_handler, 0, {}


@callback(
    Output('bin-tree', 'figure'),
    Input('pagination', 'active_page'),
    Input('bin-tree', 'figure')
)
def update_figure(active_page, bin_tree_figure):
    if active_page == 2:

        # updated_metada = metadata_by(active_page)
        bin_tree_figure = Figure(bin_tree_figure)  # Has to load its data; comes as a dict from the main page.
        # bin_tree_figure.update_traces(hovertemplate=updated_metada,)

        bin_tree_figure.update_traces(marker=dict(opacity=1.0),
                                      selector=dict(marker_opacity=0.4))

    return bin_tree_figure


# def metadata_by(active_page):
#     updated_metada = node_annotations.copy()  # Will be sorted by node_created_id's.
#
#     if active_page:
#         node_indexed_id = active_page - 1  # The pages always start from 1.
#
#         node, node_created_id, reverse_node_id = mapped_nodes.get(node_indexed_id)
#
#         for index, noted_element in node_annotations:
#             node_address, node_regex_symbol, node_metadata = noted_element
#
#             if index > reverse_node_id:
#                 updated_metada[index][2] = ''
#
#     return updated_metada


if __name__ == '__main__':
    app.run(debug=True)
