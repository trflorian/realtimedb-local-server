from .models import Player


class PlayerManager:
    def __init__(self) -> None:
        """
        Initializes the PlayerManager with an empty dictionary of players.
        """
        self._players: dict[int, Player] = {}

    def get_players_dict(self) -> dict[int, Player]:
        """
        Returns the dictionary of players.

        Returns:
            dict[int, Player]: The dictionary of players.
        """
        return self._players

    def add_or_update_player(self, player: Player) -> None:
        """
        Adds or updates a player in the dictionary.
        If the player ID already exists, it updates the existing player.

        Args:
            player (Player): The player to add.
        """
        self._players[player.id] = player

    def remove_player(self, player_id: int) -> Player:
        """
        Removes a player from the dictionary.

        Args:
            player_id (int): The ID of the player to remove.

        Raises:
            KeyError: If the player ID does not exist in the dictionary.
        """
        if player_id in self._players:
            return self._players.pop(player_id)
        else:
            raise KeyError(f"Player with ID {player_id} not found.")
