from dash import Dash, html, dcc, Input, Output, callback
from src.components.dash_page_progression.page import DashPage
import dash_bootstrap_components as dbc


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
            style={'textAlign': 'center'},
            hidden=True
        ),

        html.Br(),
    ]))


@callback(
    Output('figure-parent', 'hidden'),
    Output('tree-page-handler', 'hidden'),
    Output('pagination', 'max_value'),
    Output('bin-tree', 'figure'),
    Input('regex-input', 'value'))
def create_figure_from(user_text_entry):
    hidden_figure, hidden_page_handler = True, True

    if user_text_entry:
        global page
        page = DashPage(user_text_entry)

        return not hidden_figure, not hidden_page_handler, page.page_quantity(), page.final_figure
    return hidden_figure, hidden_page_handler, 0, {}


def update_figure_from(button_clicked):
    pass


if __name__ == '__main__':
    app.run(debug=True)
