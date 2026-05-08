from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/api/echo")
def echo(message: Message):
    return {
        "received": message.text,
        "uppercase": message.text.upper()
    }