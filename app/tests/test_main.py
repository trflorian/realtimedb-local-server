from fastapi.testclient import TestClient

from ..game.models import Player
from ..main import app

client = TestClient(app)


def test_add_and_remove_player() -> None:
    player = Player(id=0, position_x=10, position_y=20, color="FFFFFF")

    # Add a player
    response = client.put("/players/0.json", json=player.model_dump())
    assert response.status_code == 200
    assert response.json() == player.model_dump()

    # Remove the player
    response = client.delete("/players/0.json")
    assert response.status_code == 200
    assert response.json() == player.model_dump()
