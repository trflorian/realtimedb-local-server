from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep
from pydantic import BaseModel


class Player(BaseModel):
    id: int
    position_x: float
    position_y: float
    color: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

players = {}

def wrap_players_in_firebase_json():
    return json.dumps({
        "path": "/",
        "data": players
    })

async def players_generator():
    while True:
        data = wrap_players_in_firebase_json()
        yield f"event: put\ndata: {data}\n\n"
        await sleep(0.02)


@app.get("/players")
async def root():
    return StreamingResponse(players_generator(), media_type="text/event-stream")

@app.put("/players/{player_id}")
async def update_player(player_id: int, player: Player):
    players[player_id] = {
        "id": player_id,
        "position_x": player.position_x,
        "position_y": player.position_y,
        "color": player.color,
    }
    return Response(status_code=200)


@app.delete("/players/{player_id}")
async def delete_player(player_id: int):
    players.pop(player_id)
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
