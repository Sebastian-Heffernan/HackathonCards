from backend.engine.classes.instruction import Instruction
from backend import BuildError
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# Player Variable
# VARP [SET][PLAYER ID][name][value]
def execute(instruction : Instruction, engine : GameEngine):
    if len(instruction.args) == 0:
        raise BuildError("VARP: [SET][PLAYER ID][name][value]")
    command = instruction.args[0]
    
    if command == "SET":
        if len(instruction.args) < 4:
            raise BuildError("VARP: requires 4 args")

        player_i = engine.gameState.resolve_variable(instruction.args[1])
        var_name = instruction.args[2]
        var_value = engine.gameState.resolve_variable(instruction.args[3])

        # Safety check for player index
        if not isinstance(player_i, int):
            raise BuildError(f"VARP: player index must be a valid integer")
        if player_i >= len(engine.playerStates):
            raise BuildError(f"VARP: Player index {player_i} out of range.")
        player : PlayerState = engine.playerStates[player_i]
        player.variables[var_name] = var_value #set the value
    else:
        raise BuildError(f"Unknown VARP command: {command}")
    

    
