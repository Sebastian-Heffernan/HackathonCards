from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

import backend.engine
import backend.compiler

app = FastAPI()

# the objects storing the different rules and games
games = {}
rules = {}


class Message(BaseModel):
    text: str


class GetRules(BaseModel):
    source: str


@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/api/echo")
def echo(message: Message):
    return {
        "received": message.text,
        "uppercase": message.text.upper()
    }

@app.post("/api/rules")
def get_rules(rules: GetRules):
    # recieve the rules from the client
    source = rules.source
    # pass them to the json compiler
    #json_rules = backend.compiler.compile(source)
    # store in dict to reference when game starts
    rule_id = str(uuid4())
    #rules[rule_id] = json_rules

    return {
        "ok": True,
        "ruleId": rule_id
        }
