from dash import Dash, html, dcc
from src.components.dash_tree.figure import figure


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Rosetta', style={'textAlign': 'center'}),
    dcc.Input(style={'textAlign': 'center'}),
    dcc.Graph(figure=figure())
])

if __name__ == '__main__':
    app.run(debug=True)
