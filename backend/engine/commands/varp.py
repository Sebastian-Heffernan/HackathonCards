from backend.engine.classes.instruction import Instruction
from backend import BuildError
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# Player Variable
# VARP [SET/MAKE][name][value]
def execute(instruction : Instruction, engine : GameEngine):
    if len(instruction.args) < 3:
        raise BuildError
    command = instruction.args[0]
    name = instruction.args[1]
    value = instruction.args[2]
    #if command == "SET":
    #    engine.playerStates