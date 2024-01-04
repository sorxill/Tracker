"""
Main endpoint
"""
from fastapi import FastAPI

tracker = FastAPI(
    title="Tracker",
    description="Special tracker with Telegram bot assistance",
)


@tracker.get("/")
def start_answer():
    """
    Check the tests and e.t.c
    """
    return {
        "answer": "Success",
    }
