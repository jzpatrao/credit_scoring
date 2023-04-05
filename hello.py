from fastapi import FastAPI
import uvicorn

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.graph_objs as go

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H1("Credit Scoring",className='text-center mb-4'),
    
    dbc.Row([])
    
    dbc.Row([]),
    ],
    fluid=True,
)


if __name__ == "__main__":
    uvicorn.run(app)