import uvicorn
from fastapi import Depends, FastAPI

from .game.manager import PlayerManager
from .routers import players

app = FastAPI()

app.include_router(
    players.router,
    dependencies=[Depends(PlayerManager)],
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
