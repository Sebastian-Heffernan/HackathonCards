from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

#END_TURN [next player index / None]
def execute(instruction : Instruction, engine: GameEngine):
    print("ending turn")
    gameState : GameState = engine.gameState
    if instruction.args:
        if len(instruction.args) == 1:
            gameState.turnPlayer = engine.gameState.resolve_variable(instruction.args[0])
        elif len(instruction.args) == 3:
            left = engine.gameState.resolve_variable(instruction.args[0])
            right = engine.gameState.resolve_variable(instruction.args[3])
            operator = instruction.args[1]
            if operator == "+":
                gameState.turnPlayer = left + right
            elif operator == "-":
                gameState.turnPlayer = left - right
            else:
                gameState.turnPlayer = left #pick as default
    return "break"