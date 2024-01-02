from fastapi import FastAPI

tracker = FastAPI(
    title="Tracker",
    description="Special tracker with Telegram bot assistance",
)


@tracker.get("/")
def start_answer():
    return {
        "answer": "Success",
    }
