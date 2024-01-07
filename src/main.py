"""
Main endpoint
"""

import uvicorn
from fastapi import FastAPI

from src.api.handlers import user_router

tracker = FastAPI(
    title="Tracker",
    description="Special tracker with Telegram bot assistance",
)

tracker.include_router(user_router)


@tracker.get("/")
def start_answer():
    """
    Check the tests and e.t.c
    """
    return {
        "answer": "Success",
    }


# This endpoint only for local testing.
# When u will push dev branch to main clear it.
if __name__ == "__main__":
    uvicorn.run("main:tracker", host="0.0.0.0", reload=True)
