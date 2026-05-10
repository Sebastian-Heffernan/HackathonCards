from backend import BuildError
from backend.engine.classes.deck import *
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine

"""
CALL:
    starts processing label
"""


# CALL [label: str]
def execute(instruction: Instruction, engine: GameEngine):
    arg_count = len(instruction.args)
    if arg_count < 1:
        raise BuildError("CALL [label: str] (Usage)")
    return_address = (engine.label, engine.pointer + 1)  # where to come back to
    engine.stack.append(return_address)

    # normal GOTO
    new_label = instruction.args[0]
    if new_label not in engine.rules.labels:
          raise BuildError("GOTO: Invalid label")
    engine.label = instruction.args[0]
    engine.pointer = 0
    return "jump"
