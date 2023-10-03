from dash import Dash, html, dcc, Input, Output, callback
from src.components.dash_tree.figure import figure_from
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
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
        )
    ]))


@callback(
    Output('figure-parent', 'hidden'),
    Output('bin-tree', 'figure'),
    Input('regex-input', 'value'))
def update_figure_from(value):
    hidden = True

    if value:
        return not hidden, figure_from(value)
    return hidden, {}


if __name__ == '__main__':
    app.run(debug=True)
