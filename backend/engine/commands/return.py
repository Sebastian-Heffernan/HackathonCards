from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *
from backend.engine.classes.deck import *
from backend.errors.BuildError import BuildError

# RETURN
def execute(instruction : Instruction, engine: GameEngine):
    if not engine.stack:
        raise BuildError("RETURN called with empty stack")
    prev_label, prev_pointer = engine.stack.pop()
    engine.label = prev_label
    engine.pointer = prev_pointer
    return "jump"