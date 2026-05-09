from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# GOTO [LABEL]
def execute(instruction : Instruction, engine: GameEngine):
    engine.pointer = 0
    engine.label = instruction.args[0]
    return "jump"