import random

from backend.engine.TESTING.errors.BuildError import BuildError
from backend.engine.TESTING.classesOld.deck import *
from backend.engine.TESTING.classesOld.instruction import Instruction
from backend.engine.TESTING.classesOld.states import *
from backend.engine.TESTING.engine import GameEngine

"""
DECK:
    Controls a specified deck by 
    name through an action specified
"""


# DECK [MAKE/SHUFFLE/CLEAR/RESET][name]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 2:
        raise BuildError("DECK: [MAKE | SHUFFLE | CLEAR | RESET][name] (Usage)")
    command = instruction.args[0]
    name = instruction.args[1]
    if command == "MAKE":
        if engine.get_deck(name):
            raise BuildError("DECK: deck with such name already exists")
        engine.decks.append(Deck(name))
    elif command == "SHUFFLE":
        if not engine.get_deck(name):
            raise BufferError("DECK SHUFFLE: deck does not exist")
        random.seed()
        random.shuffle(engine.get_deck(name).cards)
    elif command == "CLEAR":
        if not engine.get_deck(name):
            raise BufferError("DECK CLEAR: deck does not exist")
        engine.get_deck(name).cards = []
    elif command == "RESET":
        if not engine.get_deck(name):
            raise BufferError("DECK RESET: deck does not exist")
        deck : Deck = engine.get_deck(name)
        deck.cards = []
        deck.populate()
    else:
        raise BuildError("DECK: [MAKE | SHUFFLE | CLEAR | RESET][name] (Usage)")

