from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

X_INDEX = 0
OP_INDEX = 1
Y_INDEX = 2


# MATH [x][op][y]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 3:
        raise BuildError()

    name = instruction.args[X_INDEX]
    x = engine.gameState.resolve_variable(name)
    y = engine.gameState.resolve_variable(instruction.args[Y_INDEX])
    operator = instruction.args[OP_INDEX]
    if operator == "+":
        x += y
    elif operator == "-":
        x -= y
    elif operator == "*":
        x *= y
    elif operator == "/":
        x /= y
    elif operator == "%":
        x %= y

    engine.gameState.variables[name] = x
