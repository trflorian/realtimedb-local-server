import json
from asyncio import sleep
from typing import AsyncGenerator

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from ..dependencies import PlayerManagerDep
from ..game.manager import PlayerManager
from ..game.models import Player

router = APIRouter()


async def players_generator(player_manager: PlayerManager) -> AsyncGenerator[str]:
    """
    A generator that yields player data in a format suitable for SSE.
    This function serializes the player data and sends it as a server-sent event.
    The data is sent every 20 milliseconds.

    Returns:
        str: The serialized player data in JSON format.
    """
    while True:
        serialized_players = {
            player_id: player.model_dump() for player_id, player in player_manager.get_players_dict().items()
        }
        data = json.dumps({"path": "/", "data": serialized_players})
        yield f"event: put\ndata: {data}\n\n"
        await sleep(0.02)


@router.get(
    path="/players.json",
    responses={
        200: {"description": "Player data streamed successfully"},
        500: {"description": "Internal server error"},
    },
    tags=["players"],
)
async def get_players(
    player_manager: PlayerManagerDep,
) -> str:
    """
    A GET endpoint that streams player data as server-sent events (SSE).
    """
    return StreamingResponse(players_generator(player_manager), media_type="text/event-stream")


@router.put(
    path="/players/{player_id}.json",
    response_model=Player,
    responses={
        200: {"description": "Player updated successfully"},
        400: {"description": "Invalid player ID"},
    },
    tags=["players"],
)
async def update_player(
    player_manager: PlayerManagerDep,
    player_id: int,
    player: Player,
) -> Player:
    """
    A PUT endpoint that updates the player data.
    This endpoint is used to update the player information.
    """
    if player_id != player.id:
        return Response(content="Player ID mismatch", status_code=400)
    player_manager.add_or_update_player(player)
    return player


@router.delete(
    path="/players/{player_id}.json",
    response_model=Player,
    responses={
        200: {"description": "Player deleted successfully"},
        404: {"description": "Player not found"},
    },
    tags=["players"],
)
async def delete_player(
    player_manager: PlayerManagerDep,
    player_id: int,
) -> Player:
    """
    A DELETE endpoint that removes a player from the server.
    This endpoint is used to delete a player by their ID.
    """
    try:
        player = player_manager.remove_player(player_id)
    except KeyError:
        return Response(content="Player not found", status_code=404)

    return player
