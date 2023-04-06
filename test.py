from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
from pathlib import Path
import shap
import plotly.graph_objs as go
import numpy as np
from model import get_score

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

client_options = [{'label': str(x), 'value': x} for x in df['SK_ID_CURR'].unique()]

select_client = html.Div([
    dcc.Dropdown(
        id="client_id",
        options=client_options,
        multi=False,
        value=100001
    )
])
    

client_profile = html.Div([
    dbc.Row([
        html.Span("Income type: ", style={"font-weight": "bold"}),
        html.Div(title='Income type', id='Income type', children=[])
    ]),
    dbc.Row([
        html.Span("Education type: ", style={"font-weight": "bold"}),
        html.Div(title='Education type', id='Education type', children=[])
    ]),
    dbc.Row([
        html.Span("Region rating: ", style={"font-weight": "bold"}),
        html.Div(title='Region rating client', id='Region rating client', children=[])
    ]),
    dbc.Row([
        html.Span("Days since birth: ", style={"font-weight": "bold"}),
        html.Div(title='Days birth', id='Days birth', children=[])
    ]),
    dbc.Row([
        html.Span("Employment length: ", style={"font-weight": "bold"}),
        html.Div(title='Days employed percent', id='Days employed percent', children=[])
    ]),
    dbc.Row([
        html.Span("Ext source 1: ", style={"font-weight": "bold"}),
        html.Div(title='Ext source 1', id='Ext source 1', children=[])
    ]),
    dbc.Row([
        html.Span("Ext source 2: ", style={"font-weight": "bold"}),
        html.Div(title='Ext source 2', id='Ext source 2', children=[])
    ]),
    dbc.Row([
        html.Span("Ext source: ", style={"font-weight": "bold"}),
        html.Div(title='Ext source 3', id='Ext source 3', children=[])
    ])
])


app.layout = dbc.Container([
    html.H1("Credit Scoring", className='text-center mb-4'),
    dbc.Row([
        dbc.Col(dbc.Card([
                dbc.CardHeader("Select Client ID",
                               style={"background-color": "#1A85FF", "color": "white"}),
                select_client,
                dbc.CardBody(dcc.Graph(id="gauge-chart"))
            ]), width=6),
        dbc.Col(dbc.Card([
                dbc.CardHeader("Client Profile",
                               style={"background-color": "#1A85FF", "color": "white"}),
                client_profile
            ]), width=6)
    ], className='text-center mb-4', align='stretch'),
    dbc.Row(dbc.Col(html.Div(id='shap')), align="center"),
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
        Output("gauge-chart", "figure"),
        Output("shap", "children")
    ],
    [Input(component_id='client_id', component_property='value')]
)
def filter_df(client_id):
    """Filters the data based on the selected client ID and returns the income type and SHAP force plot."""
    
    data = df[df['SK_ID_CURR'] == client_id]
    idx = data.index.values
   
    results = get_score(data)
    risk_score = results["risk_score"]
    status = results["application_status"]

    Output1 = html.Div(data['NAME_INCOME_TYPE'])
    Output2 = html.Div(data['NAME_EDUCATION_TYPE'])
    Output3 = html.Div(data['REGION_RATING_CLIENT'])
    Output4 = html.Div(data['DAYS_BIRTH'])
    Output5 = html.Div(data['DAYS_EMPLOYED_PERC'])
    Output6 = html.Div(data['EXT_SOURCE_1'])
    Output7 = html.Div(data['EXT_SOURCE_2'])
    Output8 = html.Div(data['EXT_SOURCE_3'])

    fig_gauge = go.Figure(go.Indicator(domain={'x': [0, 1], 'y': [0, 1]},
                                 value=np.around(risk_score, 2),
                                 mode="gauge+number",
                                 title={'text': f"{status}", 'font': {'size': 24}},
                                 gauge={'axis': {'range': [0, 1], 'tickwidth': 2, 'tickcolor': "grey"},
                                        'bar': {'color': "black"},'bordercolor': "black",
                                        'steps': [{'range': [0, 0.33], 'color': "#1A85FF"}, #using colorblind friendly colors
                                                  {'range': [0.33, 1], 'color': "#D41159"}],
                                        'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 0.33}}))
    shap_html = get_force_plot_html(shap_values[idx])

    return Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8, fig_gauge, shap_html


if __name__ == '__main__':
    app.run_server(debug=True)