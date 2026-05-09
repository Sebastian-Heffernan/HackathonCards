from backend.engine.classes.instruction import Instruction
from backend import BuildError
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# Game Variable
# VARG [SET][name][value]
def execute(instruction : Instruction, engine : GameEngine):
    if len(instruction.args) == 0:
        raise BuildError("VARG requires at least 1 arg")
    command = instruction.args[0]
    
    if command == "SET":
        if len(instruction.args) < 3:
            raise BuildError("VARG SET requires 2 args")

        var_name = instruction.args[1]
        var_value = engine.gameState.resolve_variable(instruction.args[2])

        engine.gameState.variables[var_name] = var_value #set the value
    else:
        raise BuildError(f"Unknown VARG command: {command}")
    

    
