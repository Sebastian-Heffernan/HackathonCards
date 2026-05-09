from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *
from backend.engine.classes.deck import *
from backend.BuildError import BuildError
import random

# DECK [MAKE/SHUFFLE][name]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) < 2:
        raise BuildError()
    command = instruction.args[0]
    name = instruction.args[1]
    if command == "MAKE":
        if engine.get_deck(name):
            raise BuildError()
        engine.decks.append(Deck(name))
    elif command == "SHUFFLE":
        random.shuffle(engine.get_deck(name).cards)
    else:
        raise BuildError()