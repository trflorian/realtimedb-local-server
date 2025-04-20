# Realtime DB Local Server

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![GitHub License](https://img.shields.io/github/license/trflorian/ball-tracking-live-plot?style=flat)

A tiny web server with three endpoints:

- @app.put("/players/{player_id}.json")
- @app.delete("/players/{player_id}.json")
- @app.get("/players.json")

The `player.json` endpoint implements the server-sent event protocol, similar to how the Firebase Realtime DB sends data to clients when something changes.
All players are sent at a regular interval regardless of whether their data has changed.

This project is part of the multiplayer firebase project:
- https://github.com/trflorian/multiplayer-firebase
