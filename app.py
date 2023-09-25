from dash import Dash, html, dcc
from src.components.dash_tree.figure import figure
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H1(children='Rosetta', style={'textAlign': 'center'}),

        html.Br(),
        html.Br(),

        html.Div(children=[
            dcc.Input(
                placeholder='Type your favorite regex!',
                debounce=True),
        ], style={"display": "flex", "justifyContent": "center"},
        ),

        html.Br(),

        html.Div(children=[dcc.Graph(figure=figure())])
    ]))


if __name__ == '__main__':
    app.run(debug=True)
