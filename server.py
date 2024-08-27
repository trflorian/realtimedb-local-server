from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
import json

players = {}
streaming_clients: list[HTTPConnection] = []

# create a simple server with the following two endpoints:
# 1. /PLAYER_ID.json: PUT request -> sets the player data for the given player id
# 2. /players.json: POST with text/event-stream -> starts the server-sent event stream for all players


# EVENT FOR SINGLE PLAYER
# event: put
# data: {"path": "/PLAYER001", "data": {"PLAYER001": "1", "x": 10, "y": 20}}

# EVENT FOR ALL PLAYERS
# event: put
# data: {"path": "/", "data": {"PLAYER001": "1", "x": 10, "y": 20}, "PLAYER002": "2", "x": 30, "y": 40}

def encode_single_player_event_data(player_id: str) -> str:
    return "\n".join([
        "event: put",
        "data: " + json.dumps({
            "path": f"/{player_id}",
            "data": players[player_id]
        })
    ]) + "\n\n"

def encode_all_players_event_data() -> str:
    return "\n".join([
        "event: put",
        "data: " + json.dumps({
            "path": "/",
            "data": players
        })
    ]) + "\n\n"

def handle_put_player_data(player_id: str, data: dict):
    players[player_id] = data

    event_data = encode_single_player_event_data(player_id)

    # for client in streaming_clients:
    #     client.send(event_data.encode())


class GameServerRequestHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        player_id = self.path[1:-5]
        data = json.loads(self.rfile.read().decode())
        handle_put_player_data(player_id, data)

    def do_POST(self):
        self.handle_post_players_streaming()
        self.send_response(200)

    def handle_post_players_streaming(self):
        self.send_response(200)

        streaming_clients.append(self.wfile)

        event_data = encode_all_players_event_data()
        self.wfile.write(event_data.encode())

def run():
    server = HTTPServer(("localhost", 8080), GameServerRequestHandler)
    print(f"Server started at http://{server.server_address[0]}:{server.server_address[1]}")
    server.serve_forever()

if __name__ == "__main__":
    run()