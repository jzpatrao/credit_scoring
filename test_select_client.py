from dashboard import select_client

def test_select_client():
    client_id = 100003
    expected_output = {'label': '100003', 'value': 100003}
    select_client_dropdown = select_client.children[0]
    assert select_client_dropdown.options[2] == expected_output