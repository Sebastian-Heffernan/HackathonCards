from errors.BuildError import BuildError
from engine.classes.deck import *
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.engine import GameEngine

# RETURN
def execute(instruction : Instruction, engine: GameEngine):
    if not engine.stack:
        raise BuildError("RETURN called with empty stack")
    prev_label, prev_pointer = engine.stack.pop()
    engine.label = prev_label
    engine.pointer = prev_pointer
    return "jump"