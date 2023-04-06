from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])

server = app.server

app.layout = dbc.Container([
    html.H1("Credit Scoring",className='text-center mb-4')
                            ])

# @app.callback(Output('display-value', 'children'),
#                 [Input('dropdown', 'value')])
# def display_value(value):
#     return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)