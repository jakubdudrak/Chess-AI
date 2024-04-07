import requests
import json

def send_fen_to_server(fen, mode="bestmove", depth=5):
    print("Sending Request to Server")
    base_url = "http://localhost:8080/api/calculateMove"
    params = {
        "fen": fen,
        "mode": mode,
        "depth": depth
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
        if 'data' in response_data and "bestmove" in response_data['data']:
            data_string = response_data['data']
            move = data_string.split()[1]
            return move if move != '(none)' else None
        else:
            print("No valid 'bestmove' found in the response.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")
        return None
