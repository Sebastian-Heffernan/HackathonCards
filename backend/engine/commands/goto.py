from backend.engine.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.states import *

# GOTO [LABEL]
def execute(instruction : Instruction, engine: GameEngine):
    engine.pointer = -1
    engine.label = instruction.args[0]