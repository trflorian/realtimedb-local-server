import json
from asyncio import sleep
from typing import AsyncGenerator

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()


class Player(BaseModel):
    id: int
    position_x: float
    position_y: float
    color: str


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


@router.get(
    path="/players.json",
)
async def get_players() -> StreamingResponse:
    """
    A GET endpoint that streams player data as server-sent events (SSE).
    """
    return StreamingResponse(players_generator(), media_type="text/event-stream")


@router.put(
    path="/players/{player_id}.json",
)
async def update_player(
    player_id: int,
    player: Player,
) -> Response:
    """
    A PUT endpoint that updates the player data.
    This endpoint is used to update the player information.
    """
    players[player_id] = player
    return Response(status_code=200)


@router.delete(
    path="/players/{player_id}.json",
)
async def delete_player(player_id: int) -> Response:
    """
    A DELETE endpoint that removes a player from the server.
    This endpoint is used to delete a player by their ID.
    """
    if player_id not in players:
        return Response(status_code=404)
    players.pop(player_id)
    return Response(status_code=200)
