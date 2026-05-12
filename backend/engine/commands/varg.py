from errors.BuildError import BuildError
from backend.engine.TESTING.classesOld.deck import Deck
from backend.engine.TESTING.classesOld.instruction import Instruction
from backend.engine.TESTING.classesOld.states import *
from engine.engine import GameEngine

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
    elif command == "PLAYER":
        #load value from current player into global variable
        #VARG PLAYER P[PLAYER ID][VAR NAME]
        var_name = instruction.args[2]
        var_player_index = engine.gameState.resolve_variable(instruction.args[1])
        var_value = engine.playerStates[var_player_index].resolve_variable(var_name)

        engine.gameState.variables[var_name] = var_value
    else:
        raise BuildError(f"Unknown VARG command: {command}")
    

    
