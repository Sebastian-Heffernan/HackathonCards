from errors.BuildError import BuildError
from engine.classes.deck import Deck
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.engine import GameEngine

# GETATR [VAR] [PATH]
def execute(instruction : Instruction, engine : GameEngine):
    if len(instruction.args) != 2:
            raise BuildError("GETATR [VAR][PATH] (Usage)")
    var_name = instruction.args[0]
    path = instruction.args[1]
    try:
        value = engine.resolve_path(engine, path)
        engine.gameState.variables[var_name] = value #set the value
    except:
        raise BuildError("GETATR: Incorrect path")