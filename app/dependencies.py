from typing import Annotated

from fastapi import Depends

from .game.manager import PlayerManager

player_manager_instance = PlayerManager()


async def get_player_manager() -> PlayerManager:
    """
    Dependency that provides a singleton instance of PlayerManager.

    Returns:
        PlayerManager: The singleton instance of PlayerManager.
    """
    return player_manager_instance


# Shared instance of PlayerManager
PlayerManagerDep = Annotated[PlayerManager, Depends(get_player_manager)]
