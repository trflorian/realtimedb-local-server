import uvicorn
from fastapi import FastAPI

from .routers import players

app = FastAPI()

app.include_router(
    players.router,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
