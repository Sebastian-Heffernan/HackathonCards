from backend.errors.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

"""
COMPARE: 
    Sets x = x + y for COMPARE x + y
    On true executes n+1. On false, n+2
    COMPARE x + y
    GOTO TRUE
    GOTO FALSE
"""

def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError("COMPARE: [x][operator][y] (Usage)")
    left = engine.gameState.resolve_variable(instruction.args[0])
    right = engine.gameState.resolve_variable(instruction.args[2])
    operator = instruction.args[1]
    if(engine.debug):
        print(f"Comparing {left} {operator} {right}")
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
        raise BuildError("COMPARE: [operator]: == | != | > | < | >= | <=")
    if not condition_met:
        engine.pointer += 1  # skip a step on false
