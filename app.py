from dash import Dash, html, dcc, Input, Output, callback, dash
from src.components.dash_page_progression.page import DashPage
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure

page = DashPage.empty_dash_page()

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
            style={'display': 'flex', 'justifyContent': 'center'},
            hidden=True
        ),

        html.Br(),
        html.Br(),

        html.Div(
            id='follow-pos-table-parent',
            children=[
                dash.dash_table.DataTable(
                        id='follow-pos-table',
                        columns=[{'name': i, 'id': i} for i in ['Node n', 'follow_pos(n)']],
                        data=[],
                    ),
            ],
            style={'display': 'flex', 'justifyContent': 'center'},
            hidden=True,
        )
    ]))


@callback(
    Output('figure-parent', 'hidden'),
    Output('tree-page-handler', 'hidden'),
    Output('follow-pos-table-parent', 'hidden'),

    Output('pagination', 'max_value'),
    Output('bin-tree', 'figure', allow_duplicate=True),
    Output('follow-pos-table', 'data'),

    Input('regex-input', 'value'),
    prevent_initial_call=True)
def create_figure_from(user_text_entry):
    hidden_figure, hidden_page_handler, hidden_follow_pos_figure = True, True, True

    if user_text_entry:
        global page
        page = DashPage(user_text_entry)

        return (not hidden_figure,
                not hidden_page_handler,
                not hidden_follow_pos_figure,

                page.page_quantity(),
                page.final_figure,
                [])
    return (hidden_figure,
            hidden_page_handler,
            hidden_follow_pos_figure,

            0,
            {},
            [])


@callback(
    Output('bin-tree', 'figure'),

    Input('pagination', 'active_page'),
    Input('bin-tree', 'figure')
)
def update_figure(active_page, bin_tree_figure):
    bin_tree_figure = Figure(bin_tree_figure)  # Has to load its data; comes as a dict from the main page.

    if active_page:
        page_note = page.pagination_notes()[active_page - 1].values()

        opacity = page.opacities()[active_page - 1].values()

        bin_tree_figure.update_traces(hovertemplate=list(page_note))
        bin_tree_figure.update_traces(marker=dict(opacity=list(opacity)))

    else:
        bin_tree_figure.update_traces(hoverinfo='none')

    return bin_tree_figure


if __name__ == '__main__':
    app.run(debug=True)
