from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *
from backend.engine.classes.deck import *

# DECK [MAKE/SHUFFLE][name]
def execute(instruction : Instruction, engine: GameEngine):
    command = instruction.args[0]
    name = instruction.args[1]
    if command == "MAKE":
        if not name in engine.decks
    elif command == "SHUFFLE":

    else:
        print("Unrecongnised command")