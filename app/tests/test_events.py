from ..game.models import Player
from ..sse.events import FirebaseEvent, FirebaseEventType, players_to_event


def test_players_to_event() -> None:
    """
    Test the players_to_event function.
    """
    # Create a list of Player objects
    players = [
        Player(id=0, position_x=10, position_y=20, color="FFFFFF"),
        Player(id=1, position_x=30, position_y=40, color="000000"),
    ]

    # Call the function to test
    event = players_to_event(players)

    # Check the event type
    assert event.event_type == FirebaseEventType.PUT

    # Check the event data
    expected_data = {
        "path": "/",
        "data": {
            0: {"id": 0, "position_x": 10, "position_y": 20, "color": "FFFFFF"},
            1: {"id": 1, "position_x": 30, "position_y": 40, "color": "000000"},
        },
    }
    assert event.event_data == expected_data


def test_serialize_empty_event() -> None:
    """
    Test the serialization of FirebaseEvent.
    """
    # Create a FirebaseEvent object
    event = FirebaseEvent(
        event_type=FirebaseEventType.PUT,
        event_data={"path": "/", "data": {}},
    )

    # Call the serialize method
    serialized_event = event.serialize()

    # Check the serialized format
    expected_format = 'event: put\ndata: {"path": "/", "data": {}}\n\n'
    assert serialized_event == expected_format


def test_serialize_event_with_data() -> None:
    """
    Test the serialization of FirebaseEvent with data.
    """
    # Create a FirebaseEvent object
    event = FirebaseEvent(
        event_type=FirebaseEventType.PATCH,
        event_data={"path": "/player/1", "data": {"position_x": 100, "position_y": 200}},
    )

    # Call the serialize method
    serialized_event = event.serialize()

    # Check the serialized format
    expected_format = 'event: patch\ndata: {"path": "/player/1", "data": {"position_x": 100, "position_y": 200}}\n\n'
    assert serialized_event == expected_format
