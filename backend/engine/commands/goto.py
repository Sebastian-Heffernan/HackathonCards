from errors.BuildError import BuildError
from engine.classes.deck import Deck
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.engine import GameEngine

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