import json

from asyncio import sleep
from pydantic import BaseModel

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse


class Player(BaseModel):
    id: int
    position_x: float
    position_y: float
    color: str


app = FastAPI()

players: dict[int, Player] = {}


async def players_generator():
    while True:
        serialized_players = {
            player_id: player.model_dump() for player_id, player in players.items()
        }
        data = json.dumps({"path": "/", "data": serialized_players})()
        yield f"event: put\ndata: {data}\n\n"
        await sleep(0.02)


@app.get("/players.json")
async def root():
    return StreamingResponse(players_generator(), media_type="text/event-stream")


@app.put("/players/{player_id}.json")
async def update_player(player_id: int, player: Player):
    players[player_id] = player
    return Response(status_code=200)


@app.delete("/players/{player_id}.json")
async def delete_player(player_id: int):
    if player_id not in players:
        return Response(status_code=404)
    players.pop(player_id)
    return Response(status_code=200)
