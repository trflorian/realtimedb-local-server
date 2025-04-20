import json
from dataclasses import dataclass
from enum import Enum

from app.game.models import Player


class FirebaseEventType(str, Enum):
    """
    Enum representing different types of Firebase events.
    """

    PUT = "put"
    PATCH = "patch"


@dataclass(frozen=True)
class FirebaseEvent:
    event_type: FirebaseEventType
    event_data: dict

    def serialize(self) -> str:
        """
        Serializes the Firebase event to a string format suitable for SSE.

        The serialized format is:
        '''
        event: <event_type>
        data: <event_data>
        '''
        where <event_type> is the type of the event (e.g., "put", "patch")
        and <event_data> is the serialized data in JSON format.
        """
        event_type_str = self.event_type.value
        event_data_str = json.dumps(self.event_data)
        return f"event: {event_type_str}\ndata: {event_data_str}\n\n"


def players_to_event(players: list[Player]) -> FirebaseEvent:
    """
    Converts a Player object to a FirebaseEvent.
    """
    return FirebaseEvent(
        event_type=FirebaseEventType.PUT,
        event_data={
            "path": "/",
            "data": {player.id: player.model_dump() for player in players},
        },
    )
