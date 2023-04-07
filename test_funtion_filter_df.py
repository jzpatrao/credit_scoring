import pytest
from dashboard import filter_df

def test_filter_df():
    client_id = 100001
    expected_output = (
        html.Div('Working'),
        html.Div('Secondary / secondary special'),
        html.Div(2),
        html.Div(28),
        html.Div(0.18),
        html.Div(0.51),
        html.Div(0.44),
        html.Div(0.81),
        go.Figure(go.Indicator(domain={'x': [0, 1], 'y': [0, 1]},
                         value=0.52,
                         mode="gauge+number",
                         title={'text': 'Approved', 'font': {'size': 24}},
                         gauge={'axis': {'range': [0, 1], 'tickwidth': 2, 'tickcolor': "grey"},
                                'bar': {'color': "black"},'bordercolor': "black",
                                'steps': [{'range': [0, 0.33], 'color': "#1A85FF"},
                                          {'range': [0.33, 1], 'color': "#D41159"}],
                                'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 0.33}})),
    )
    
    output = filter_df(client_id)
    
    assert output == expected_output
