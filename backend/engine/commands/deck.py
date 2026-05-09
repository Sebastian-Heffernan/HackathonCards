from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *
from backend.engine.classes.deck import *
from backend import BuildError
import random

# DECK [MAKE/SHUFFLE][name]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError
    command = instruction.args[0]
    name = instruction.args[1]
    if command == "MAKE":
        for deck in engine.decks:
            if deck.name == name:
                raise BuildError()
        engine.decks.append(Deck(name))
    elif command == "SHUFFLE":
         for deck in engine.decks:
            if deck.name == name:
                random.shuffle(deck.cards)
    else:
        raise BuildError()