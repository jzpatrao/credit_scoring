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
@app.callback(
    [
        Output(component_id='Income type', component_property='children'),
        Output(component_id='Education type', component_property='children'),
        Output(component_id='Region rating client',
               component_property='children'),
        Output(component_id='Days birth', component_property='children'),
        Output(component_id='Days employed percent',
               component_property='children'),
        Output(component_id='Ext source 1', component_property='children'),
        Output(component_id='Ext source 2', component_property='children'),
        Output(component_id='Ext source 3', component_property='children'),
    ],
    [Input(component_id='Client ID', component_property='value')]
)
def filter_df(client_id):
    
    data = df[df['SK_ID_CURR'] == client_id]

    Output1 = data['NAME_INCOME_TYPE']
    Output2 = data['NAME_EDUCATION_TYPE']
    Output3 = data['REGION_RATING_CLIENT']
    Output4 = data['DAYS_BIRTH']
    Output5 = data['DAYS_EMPLOYED_PERC']
    Output6 = data['EXT_SOURCE_1']
    Output7 = data['EXT_SOURCE_2']
    Output8 = data['EXT_SOURCE_3']

    return Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8

if __name__ == '__main__':
    app.run_server(debug=True)