from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
from pathlib import Path
import shap

BASE_DIR = Path(__file__).resolve(strict=True).parent

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])

server = app.server

df = pd.read_csv("application_test.csv")

with open(BASE_DIR.joinpath("shap_values_test_set.pkl"), "rb") as f:
    shap_values = pickle.load(f)

def get_force_plot_html(*args):
    """Returns a SHAP force plot as an HTML iframe."""
    force_plot = shap.force_plot(*args, matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    return html.Iframe(srcDoc=shap_html, style={"width": "100%", "height": "600px", "border": 1})

client_options = df['SK_ID_CURR'].apply(lambda x: {'label': x, 'value': x}).to_list()

select_client = html.Div([
    dbc.Label("Client ID"),
    dcc.Dropdown(id="client_id", options=client_options, multi=False, value=100001)
])
    

client_profile = [
	dbc.Row(html.Div(title='Income type', id='Income type', children=[])),
	dbc.Row(html.Div(title='Education type',id='Education type', children=[])),
      dbc.Row(html.Div(title='Region rating client',id='Region rating client', children=[])),
      dbc.Row(html.Div(title='Days birth',id='Days birth', children=[])),
      dbc.Row(html.Div(title='Days employed percent',id='Days employed percent', children=[])),
      dbc.Row(html.Div(title='Ext source 1',id='Ext source 1', children=[])),
      dbc.Row(html.Div(title='Ext source 2',id='Ext source 2', children=[])),
      dbc.Row(html.Div(title='Ext source 3',id='Ext source 3', children=[]))
]

app.layout = dbc.Container([
    html.H1("Credit Scoring", className='text-center mb-4'),
    dbc.Row([
        dbc.Col(dbc.Card(select_client), width=6),
        dbc.Col(dbc.Card(client_profile), width=6)
    ], className='text-center mb-4'),
    dbc.Row([
        dbc.Row(html.Div(id='shap'))
    ], align="center"),
], fluid=True)

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
        Output("shap", "children")
    ],
    [Input(component_id='client_id', component_property='value')]
)
def filter_df(client_id):
    """Filters the data based on the selected client ID and returns the income type and SHAP force plot."""
    
    data = df[df['SK_ID_CURR'] == client_id]
    idx = data.index.values

    Output1 = data['NAME_INCOME_TYPE']
    Output2 = data['NAME_EDUCATION_TYPE']
    Output3 = data['REGION_RATING_CLIENT']
    Output4 = data['DAYS_BIRTH']
    Output5 = data['DAYS_EMPLOYED_PERC']
    Output6 = data['EXT_SOURCE_1']
    Output7 = data['EXT_SOURCE_2']
    Output8 = data['EXT_SOURCE_3']

    shap_html = get_force_plot_html(shap_values[idx])

    return Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8, shap_html

if __name__ == '__main__':
    app.run_server(debug=True)