from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import shap
import plotly.graph_objs as go
import requests


# Get the base directory of the current file
BASE_DIR = Path(__file__).resolve(strict=True).parent

# Instantiate the dash app
app = Dash(external_stylesheets=[dbc.themes.JOURNAL])
# server = app.server
app.title = "Credit Scoring - Prêt à dépenser" 

# Load dataset and saved shap values from pickle
df = pd.read_csv("application_test.csv")

with open(BASE_DIR.joinpath("shap_values_test_set.pkl"), "rb") as f:
    shap_values = pickle.load(f)

# A function to get SHAP force plot in html format
def get_force_plot_html(*args):
    """Returns a SHAP force plot as an HTML iframe."""
    force_plot = shap.force_plot(*args, matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    return html.Iframe(srcDoc=shap_html, style={"width": "100%", "height": "600px", "border": 1})

# Define options for a dropdown box that select a client id.
client_options = [{'label': str(x), 'value': x} for x in df['SK_ID_CURR'].unique()]

# Drop down box for client selection
select_client = html.Div([
    dcc.Dropdown(
        id="client_id",
        options=client_options,
        multi=False,
        value=100001
    )
])
    
# Define client profile in detail
client_profile = html.Div([
    dbc.Row([
        html.Span("Income type: ", style={"font-weight": "bold"}),
        html.Div(title='Income type', id='Income type', children=[])
    ]),
    dbc.Row([
        html.Span("Days credit: ", style={"font-weight": "bold"}),
        html.Div(title='Days credit', id='Days credit', children=[])
    ]),
    dbc.Row([
        html.Span("Region rating: ", style={"font-weight": "bold"}),
        html.Div(title='Region rating client', id='Region rating client', children=[])
    ]),
    dbc.Row([
        html.Span("Age: ", style={"font-weight": "bold"}),
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

# Define dashboard layout
app.layout = dbc.Container([
    html.H1("Credit Scoring", className='text-center mb-2'), # Page title
    html.H4("Prêt à dépenser", className='text-center mb-4', style={'padding-bottom': '10px'}), # Subtitle
    dbc.Row([
        dbc.Col(dbc.Card([
                dbc.CardHeader("Select Client ID",
                               style={"background-color": "#1A85FF", "color": "white", "font-weight": "bold"}),
                select_client,
                dbc.CardBody(dcc.Graph(id="gauge-chart"))
            ], className='mb-4', style={"height": "100%"}), width=6), # Card component with a dropdown box and a gauge chart
        dbc.Col(dbc.Card([
                dbc.CardHeader("Client Profile",
                               style={"background-color": "#1A85FF", "color": "white", "font-weight": "bold"}),
                client_profile
            ], className='mb-4', style={"height": "100%"}), width=6)
    ], className='text-center', align='stretch'), # A card components displaying selected client features
    dbc.Row([
        dbc.Col(html.H4("Feature Explainer (SHAP)", className='text-center mb-4'), width=12,
                style={"padding-top": "20px"}), # Title for SHAP plot
    ]),
    dbc.Row(dbc.Col(html.Div(id='shap', 
                             style={'width': '100%', 'height': '800px'})), align="center", className='mb-4')
], fluid=True,) # SHAP force plot


# Define inputs in above layout with callbacks.
@app.callback(
    [
        Output(component_id='Income type', component_property='children'),
        Output(component_id='Days credit', component_property='children'),
        Output(component_id='Region rating client',
               component_property='children'),
        Output(component_id='Days birth', component_property='children'),
        Output(component_id='Days employed percent',
               component_property='children'),
        Output(component_id='Ext source 1', component_property='children'),
        Output(component_id='Ext source 2', component_property='children'),
        Output(component_id='Ext source 3', component_property='children')
    ],
    [Input(component_id='client_id', component_property='value')]
)
def get_client_features(client_id):
    data = df[df['SK_ID_CURR'] == client_id]

    Output1 = html.Div(data['NAME_INCOME_TYPE'])
    Output2 = html.Div(data['DAYS_CREDIT'])
    Output3 = html.Div(data['REGION_RATING_CLIENT'])
    Output4 = html.Div(int(data['DAYS_BIRTH']/365))
    Output5 = html.Div(round(data['DAYS_EMPLOYED_PERC'],2))
    Output6 = html.Div(round(data['EXT_SOURCE_1'],2))
    Output7 = html.Div(round(data['EXT_SOURCE_2'],2))
    Output8 = html.Div(round(data['EXT_SOURCE_3'],2))
    return Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8


@app.callback(
    [
        Output("gauge-chart", "figure"),
        Output("shap", "children")
    ],
    [Input(component_id='client_id', component_property='value')]
)

# Define values for above callback outputs
def get_model_prediction(client_id):
    data = df[df['SK_ID_CURR'] == client_id]
    idx = data.index.values

    url = "https://oc-project-7-fastapi.herokuapp.com/score"
    payload = {
              "NAME_INCOME_TYPE": data['NAME_INCOME_TYPE'].item(),
              "DAYS_CREDIT": data['DAYS_CREDIT'].item(),
              "DAYS_BIRTH": data['DAYS_BIRTH'].item(),
              "DAYS_EMPLOYED_PERC": data['DAYS_EMPLOYED_PERC'].item(),
              "REGION_RATING_CLIENT": data['REGION_RATING_CLIENT'].item(),
              "EXT_SOURCE_1": data['EXT_SOURCE_1'].item(),
              "EXT_SOURCE_2": data['EXT_SOURCE_2'].item(),
              "EXT_SOURCE_3": data['EXT_SOURCE_3'].item()
            }

    response = requests.post(url, json=payload)

    data_from_api = response.json()

    risk_score = data_from_api["risk_score"]

    status = data_from_api["application_status"]

    fig_gauge = go.Figure(go.Indicator(domain={'x': [0, 1], 'y': [0, 1]},
                                 value=np.around(risk_score, 2),
                                 mode="gauge+number",
                                 title={'text': f"{status}", 'font': {'size': 24}},
                                 gauge={'axis': {'range': [0, 1], 'tickwidth': 2, 'tickcolor': "grey"},
                                        'bar': {'color': "black"},'bordercolor': "black",
                                        'steps': [{'range': [0, 0.4933], 'color': "#1A85FF"}, #using colorblind friendly colors
                                                  {'range': [0.4933, 1], 'color': "#D41159"}],
                                        'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 0.4933}}))
    shap_html = get_force_plot_html(shap_values[idx])
    
    return fig_gauge, shap_html

if __name__ == '__main__':
    app.run_server(debug=True)