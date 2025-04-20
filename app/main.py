import json
from asyncio import sleep
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class Player(BaseModel):
    id: int
    position_x: float
    position_y: float
    color: str


app = FastAPI()

players: dict[int, Player] = {}


async def players_generator() -> AsyncGenerator[str]:
    """
    A generator that yields player data in a format suitable for SSE.
    This function serializes the player data and sends it as a server-sent event.
    The data is sent every 20 milliseconds.

    Returns:
        str: The serialized player data in JSON format.
    """
    while True:
        serialized_players = {player_id: player.model_dump() for player_id, player in players.items()}
        data = json.dumps({"path": "/", "data": serialized_players})
        yield f"event: put\ndata: {data}\n\n"
        await sleep(0.02)


@app.get("/players.json")
async def root() -> StreamingResponse:
    """
    A simple GET endpoint that returns a JSON response with the player data.
    This endpoint is used to retrieve the current state of players.

    Returns:
        StreamingResponse: A streaming response that sends player data as server-sent events.
    """
    return StreamingResponse(players_generator(), media_type="text/event-stream")


@app.put("/players/{player_id}.json")
async def update_player(
    player_id: int,
    player: Player,
) -> Response:
    """
    A PUT endpoint that updates the player data.
    This endpoint is used to update the player information.

    Args:
        player_id (int): The ID of the player to update.
        player (Player): The updated player data.

    Returns:
        Response: A response indicating the status of the update.
    """
    players[player_id] = player
    return Response(status_code=200)


@app.delete("/players/{player_id}.json")
async def delete_player(player_id: int) -> Response:
    """
    A DELETE endpoint that removes a player from the server.
    This endpoint is used to delete a player by their ID.

    Args:
        player_id (int): The ID of the player to delete.

    Returns:
        Response: A response indicating the status of the deletion.
    """
    if player_id not in players:
        return Response(status_code=404)
    players.pop(player_id)
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
