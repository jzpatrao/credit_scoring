from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.FLATLY])

server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)