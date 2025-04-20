from pydantic import BaseModel


class Player(BaseModel):
    """
    A class representing a player in the game.

    Attributes:
        id (int): The unique identifier for the player.
        position_x (float): The x-coordinate of the player's position.
        position_y (float): The y-coordinate of the player's position.
        color (str): The color of the player in hexadecimal format (e.g., "FF5733").
    """

    id: int
    position_x: float
    position_y: float
    color: str
