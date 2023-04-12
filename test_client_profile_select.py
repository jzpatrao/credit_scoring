from dash import dcc, html
import dash_bootstrap_components as dbc
from dashboard import app

def test_select_client_layout():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        
        client_options = [{'label': str(x), 'value': x} for x in df['SK_ID_CURR'].unique()]
        select_client = html.Div([
            dcc.Dropdown(
                id="client_id",
                options=client_options,
                multi=False,
                value=100001
            )
        ])
        
        assert select_client in response.get_data(as_text=True)
