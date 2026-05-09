from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
import re

# (DEBUG) PRINT [ARGS]
def execute(instruction : Instruction, engine : GameEngine):
    path = instruction.args[0]

    def replace_var(match):
        var_name = match.group(1)
        # Only resolve if it's not a pure digit (leave [0] alone)
        if not var_name.isdigit():
            return f"[{engine.gameState.resolve_variable(var_name)}]"
        return f"[{var_name}]"
    resolved_path = re.sub(r"\[(\w+)\]", replace_var, path)

    #if resolved_path.startswith("playerStates"):
    value = engine.resolve_path(engine, resolved_path)
    #else:
        #value = engine.resolve_path(engine.gameState, resolved_path)
        
    print(f"DEBUG: {resolved_path} = {value}")