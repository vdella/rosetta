from dash import Dash, html, dcc, Input, Output, callback, State
from src.components.dash_tree.figure import figure_from
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H1(children='Rosetta', style={'textAlign': 'center'}),

        html.Br(),
        html.Br(),

        dcc.Input(
            id='regex-input',
            placeholder='Type your favorite regex!',
            debounce=True),

        html.Br(),

        dbc.Button('Submit', id='submit-button', style={'textAlign': 'center'}),

        html.Div(
            id='output-container-button',
            children='Enter a value and press submit'),

        html.Br(),
        html.Br(),

        html.Div(
            id="output",
            style={"verticalAlign": "middle"}),

        dcc.Graph(
            id='bin-tree',
            figure={},
        )
    ]))


@callback(
    Output('bin-tree', 'figure'),
    Input('regex-input', 'value'))
def update_output(value):
    if value:
        return figure_from(value)
    return {}


if __name__ == '__main__':
    app.run(debug=True)
