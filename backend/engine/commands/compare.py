from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

"""
COMPARE: 
    Sets x = x + y for COMPARE x + y
    On true executes n+1. On false, n+2
"""


# COMPARE [x][operator][y]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError()
    left = engine.gameState.resolve_variable(instruction.args[0])
    right = engine.gameState.resolve_variable(instruction.args[2])
    print(right)
    operator = instruction.args[1]
    condition_met = False
    if operator == "==":
        condition_met = left == right
    elif operator == "!=":
        condition_met = left != right
    elif operator == ">":
        condition_met = left > right
    elif operator == "<":
        condition_met = left < right
    elif operator == ">=":
        condition_met = left >= right
    elif operator == "<=":
        condition_met = left <= right
    else:
        raise BuildError()
    if not condition_met:
        engine.pointer += 1  # skip a step on false
