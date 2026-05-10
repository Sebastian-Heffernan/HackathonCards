from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# GOTO [LABEL]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
            raise BuildError("GOTO [LABEL] (Usage)")
    new_label = instruction.args[0]
    if new_label not in engine.rules.labels:
          raise BuildError("GOTO: Invalid label")
    engine.label = new_label
    engine.pointer = 0
    return "jump"