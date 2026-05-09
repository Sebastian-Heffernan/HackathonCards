from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *
from backend.engine.classes.deck import *

# CALL [LABEL]
def execute(instruction : Instruction, engine: GameEngine):
    return_address = (engine.label, engine.pointer + 1) #where to come back to
    engine.stack.append(return_address)

    #normal GOTO
    engine.label = instruction.args[0]
    engine.pointer = -1
