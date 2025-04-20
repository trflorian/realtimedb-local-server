# Realtime DB Local Server

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![GitHub License](https://img.shields.io/github/license/trflorian/ball-tracking-live-plot?style=flat)

A tiny web server to manage player data and transmit real-time updates via Server-Sent Events (SSE).
All endpoints operate under the `/players` path.

This project is part of the multiplayer firebase project:
https://github.com/trflorian/multiplayer-firebase

## API Overview

**Endpoints:**

* **`GET /players.json`**
    * **Purpose:** Stream real-time updates of the *entire* player list via Server-Sent Events (SSE).
    * **Behavior:** Periodically pushes the full player dataset to connected clients.

* **`PUT /players/{player_id}.json`**
    * **Purpose:** Create a new player or update an existing player's data.
    * **Identifies Player By:** `player_id` in the URL path.
    * **Requires:** Player data matching the `Player` model in the request body.

* **`DELETE /players/{player_id}.json`**
    * **Purpose:** Delete a specific player.
    * **Identifies Player By:** `player_id` in the URL path.

## Quickstart

Run the project locally in develop mode using uv. This will automatically create a virtual environment for you and install the required packages.

```bash
uv run fastapi dev
```

For detailed specifications, schemas, and interactive testing, you can refer to the auto-generated documentation at the `/docs` path when you run the server locally.

## Testing

The project contains some basic unit tests and a simple test for some API endpoints. 
To run the test suite, use the following command:

```bash
uv run pytest
```
