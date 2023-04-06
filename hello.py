from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])

server = app.server

df = pd.read_csv("application_test.csv")
#------------------------------------------------------------
select_client = dbc.Card(
    [html.Div([dbc.Label("Client ID"),
               dcc.Dropdown(id="Client ID",options=df['SK_ID_CURR'].values,multi=False,value=100001)]),
    ],body=True)

app.layout = dbc.Container([
    html.H1("Credit Scoring",className='text-center mb-4'),
    dbc.Row([dbc.Col(select_client,width=12),])
    
                            ])

# @app.callback(Output('display-value', 'children'),
#                 [Input('dropdown', 'value')])
# def display_value(value):
#     return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)