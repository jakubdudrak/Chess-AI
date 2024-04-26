import requests
import json
def send_fen_to_server(fen, mode="bestmove", depth=5):
    print("Sending Request to Server")
    base_url = "http://185.150.1.180:8080/api/calculateMove"
    params = {
        "fen": fen,
        "mode": mode,
        "depth": depth
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        
    
        move_data = response.json()
        move = move_data.get('move')  
        
        if move and move != '(none)':  
            print(move)
            return move
        else:
            print("No valid 'bestmove' found in the response.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")
    return None

#send_fen_to_server('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
