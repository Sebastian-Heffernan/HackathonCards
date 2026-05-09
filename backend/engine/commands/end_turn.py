from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine

"""
END_TURN:
    Finishes the label execution initiated by action
"""


# END_TURN [next player index / None]
def execute(instruction: Instruction, engine: GameEngine):
    print("ending turn")
    gameState: GameState = engine.gameState
    if len(instruction.args) == 0:
        return "break"
    elif len(instruction.args) == 1:
        gameState.turnPlayer = engine.gameState.resolve_variable(
            instruction.args[0]
        )
    elif len(instruction.args) == 3:
        left = engine.gameState.resolve_variable(instruction.args[0])
        right = engine.gameState.resolve_variable(instruction.args[2])
        operator = instruction.args[1]
        if operator == "+":
            gameState.turnPlayer = left + right
        elif operator == "-":
            gameState.turnPlayer = left - right
        else:
            gameState.turnPlayer = left  # pick as default
    return "break"

