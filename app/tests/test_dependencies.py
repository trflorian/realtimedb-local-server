import pytest

from ..dependencies import get_player_manager


@pytest.mark.asyncio
async def test_player_manager_singleton() -> None:
    """
    Test that the PlayerManager singleton instance is the same across different imports.
    """
    player_manager1 = await get_player_manager()
    player_manager2 = await get_player_manager()

    assert player_manager1 is player_manager2, "PlayerManager instances are not the same."
