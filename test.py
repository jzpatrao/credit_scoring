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
client_profile=[dbc.Row(html.Div(title='Income type',id='Income type', children=[])),
                dbc.Row(html.Div(title='Education type',id='Education type', children=[])),
                dbc.Row(html.Div(title='Region rating client',id='Region rating client', children=[])),
                dbc.Row(html.Div(title='Days birth',id='Days birth', children=[])),
                dbc.Row(html.Div(title='Days employed percent',id='Days employed percent', children=[])),
                dbc.Row(html.Div(title='Ext source 1',id='Ext source 1', children=[])),
                dbc.Row(html.Div(title='Ext source 2',id='Ext source 2', children=[])),
                dbc.Row(html.Div(title='Ext source 3',id='Ext source 3', children=[]))]

app.layout = dbc.Container([
    html.H1("Credit Scoring",className='text-center mb-4'),
    dbc.Row([
    dbc.Col(select_client,width=12),
    dbc.Col(client_profile,width=12)],
    className='text-center mb-4'),
    ],
    fluid=True,
)


if __name__ == '__main__':
    app.run_server(debug=True)