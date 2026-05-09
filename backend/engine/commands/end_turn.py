from backend.engine.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.states import *

#END_TURN [next player index]
def execute(instruction : Instruction, engine: GameEngine):
    gameState : GameState = engine.gameState
    if instruction.args:
        if len(instruction.args) == 1:
            gameState.turnPlayer = engine.resolve_game_variable(instruction.args[0])
        elif len(instruction.args) == 3:
            left = engine.resolve_game_variable(instruction.args[0])
            right = engine.resolve_game_variable(instruction.args[3])
            operator = instruction.args[1]
            if operator == "+":
                gameState.turnPlayer = left + right
            elif operator == "-":
                gameState.turnPlayer = left - right
            else:
                gameState.turnPlayer = left #pick as default