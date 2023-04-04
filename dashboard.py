import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.graph_objs as go

import pickle
import re
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import json
import shap
from model.model import give_score

BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/shap_values_test_set.pkl", "rb") as f:
    shap_values = pickle.load(f)
    
    
############################################################################
# Read test dataset with selected features and client id.
# I have saved to processed dataset in a seperate csv file 
# because the original dataset is too big to push to github.
# Lines 24 to 36 are the codes used to process dataset.
# df = pd.read_csv("application_test.csv", usecols=['SK_ID_CURR',
#                                                   'NAME_INCOME_TYPE',
#                                                   'NAME_EDUCATION_TYPE',
#                                                   'REGION_RATING_CLIENT',
#                                                   'DAYS_BIRTH',
#                                                   'DAYS_EMPLOYED',
#                                                   'EXT_SOURCE_1',
#                                                   'EXT_SOURCE_2',
#                                                   'EXT_SOURCE_3'])

# df['DAYS_EMPLOYED_PERC'] = df['DAYS_EMPLOYED'] / df['DAYS_BIRTH']

# df.dropna(inplace=True)

df = pd.read_csv("application_test.csv")

# A function to display SHAP force plot in html
def force_plot_html(*args):
    force_plot = shap.force_plot(*args, matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    return html.Iframe(srcDoc=shap_html,
                       style={"width": "100%", "height": "600px", "border": 1})
############################################################################

dashboard = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# Define content elements

# Dropdown box for client ID selection
select_client = dbc.Card(
    [html.Div([dbc.Label("Client ID"),
               dcc.Dropdown(id="Client ID",options=df['SK_ID_CURR'].values,multi=False,value=100001)]),
    ],body=True)

# Display client profile (features selected)
client_profile=[dbc.Row(html.Div(title='Income type',id='Income type', children=[])),
                dbc.Row(html.Div(title='Education type',id='Education type', children=[])),
                dbc.Row(html.Div(title='Region rating client',id='Region rating client', children=[])),
                dbc.Row(html.Div(title='Days birth',id='Days birth', children=[])),
                dbc.Row(html.Div(title='Days employed percent',id='Days employed percent', children=[])),
                dbc.Row(html.Div(title='Ext source 1',id='Ext source 1', children=[])),
                dbc.Row(html.Div(title='Ext source 2',id='Ext source 2', children=[])),
                dbc.Row(html.Div(title='Ext source 3',id='Ext source 3', children=[]))]
# Actual layout
dashboard.layout = dbc.Container([
    html.H1("Credit Scoring",className='text-center mb-4'),
    
    dbc.Row([dbc.Col(select_client,width=12),
             dbc.Col(client_profile,width=12)],className='text-center mb-4'),
    
    dbc.Row([dbc.Col([dcc.Graph(id="gauge-chart")]),
             dbc.Row(html.Div(id='shap'))
           ],
            align="center",
        ),
    ],
    fluid=True,
)



@dashboard.callback(
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
    [Input(component_id='Client ID', component_property='value')]
)
    
             
def filter_df(client_id):
    
    data = df[df['SK_ID_CURR'] == client_id]
    idx=data.index.values
    data = data.set_index('SK_ID_CURR')
    data=data.to_json()
    client_id=str(client_id)

    Output1 = json.loads(data)['NAME_INCOME_TYPE'][client_id]
    Output2 = json.loads(data)['NAME_EDUCATION_TYPE'][client_id] 
    Output3 = json.loads(data)['REGION_RATING_CLIENT'][client_id]  
    Output4 = json.loads(data)['DAYS_BIRTH'][client_id] 
    Output5 = json.loads(data)['DAYS_EMPLOYED_PERC'][client_id] 
    Output6 = json.loads(data)['EXT_SOURCE_1'][client_id] 
    Output7 = json.loads(data)['EXT_SOURCE_2'][client_id] 
    Output8 = json.loads(data)['EXT_SOURCE_3'][client_id]
    
    #print('test log client_id: ', data )
    
    #call api route and pass data as argument
###################################################################################
# Posting inputs to scoring model api    
    # url = "http://127.0.0.1:8080/score"
    payload = {
              "NAME_INCOME_TYPE": Output1,
              "NAME_EDUCATION_TYPE": Output2,
              "DAYS_BIRTH": Output4,
              "DAYS_EMPLOYED_PERC": Output5,
              "REGION_RATING_CLIENT": Output3,
              "EXT_SOURCE_1": Output6,
              "EXT_SOURCE_2": Output7,
              "EXT_SOURCE_3": Output8
            }

    # response = requests.post(url=url, json = payload )
    
# Recieving prediction results from model api    

    data_from_api = give_score(payload)
    print("data_from_api" , data_from_api)
    
    risk_score = data_from_api["risk_score"]
    print('PRINT risk_score :', risk_score)
    
    status = data_from_api["application_status"]

    print('PRINT status :', status)
####################################################################################
# Data visualizations (a gauge chart for result score & a bar plot for shap explainer
    fig_gauge = go.Figure(go.Indicator(domain={'x': [0, 1], 'y': [0, 1]},
                                 value=np.around(risk_score, 2),
                                 mode="gauge+number",
                                 title={'text': f"{status}", 'font': {'size': 24}},
                                 gauge={'axis': {'range': [0, 1], 'tickwidth': 2, 'tickcolor': "grey"},
                                        'bar': {'color': "black"},'bordercolor': "black",
                                        'steps': [{'range': [0, 0.33], 'color': "#1A85FF"}, #using colorblind friendly colors
                                                  {'range': [0.33, 1], 'color': "#D41159"}],
                                        'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 0.33}}))
    
    shap_html = force_plot_html(shap_values[idx])
    

    return Output1, Output2, Output3, Output4, Output5, Output6, Output7, Output8, fig_gauge, shap_html


if __name__ == "__main__":
    dashboard.run_server(debug=True, port=8080)