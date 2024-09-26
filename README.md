# Realtime DB Local Server

A tiny web server with three endpoints:

- @app.put("/players/{player_id}.json")
- @app.delete("/players/{player_id}.json")
- @app.get("/players.json")

The last endpoint implements the server-sent event protocl, similar to how the Firebase Realtime DB sends data to clients when something changes.
Currently, all the players are just sent at a regular interval regardless of whether their data has changed.

This project is part of the multiplayer firebase project:
- https://github.com/trflorian/multiplayer-firebase
