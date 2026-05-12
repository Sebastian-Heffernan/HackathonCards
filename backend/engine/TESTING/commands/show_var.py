from backend.engine.TESTING.errors.BuildError import BuildError
from backend.engine.TESTING.classesOld.deck import Deck
from backend.engine.TESTING.classesOld.instruction import Instruction
from backend.engine.TESTING.classesOld.states import *
from backend.engine.TESTING.engine import GameEngine

# Adds variable to showVars array, shown to every client
# SHOW_VAR [NAME]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
        raise BuildError("SHOW_VAR [NAME] (Usage)")
    if instruction.args[0] not in engine.gameState.variables:
        raise BuildError("SHOW_VAR: Requires valid variable")
    if instruction.args[0] not in engine.gameState.showVars:
        engine.gameState.showVars.append(instruction.args[0])