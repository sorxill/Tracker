"""
Main endpoint of API
"""

import uvicorn
from fastapi import FastAPI

from src.api.handlers import routers

tracker = FastAPI(
    title="Tracker",
    description="Special tracker with Telegram bot assistance",
)

tracker.include_router(routers)


@tracker.get("/")
def start_answer():
    """
    Ping API server
    """

    return {
        "answer": "Success",
    }


# This endpoint only for local testing.
# When u will push dev branch to main clear it.
if __name__ == "__main__":
    uvicorn.run("main:tracker", host="0.0.0.0", reload=True)
