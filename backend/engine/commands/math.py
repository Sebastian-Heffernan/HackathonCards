from backend.errors.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

X_INDEX = 0
OP_INDEX = 1
Y_INDEX = 2


# MATH [x][op][y]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 3:
        raise BuildError("MATH [x][OPERATOR][y] (Usage)")

    name = instruction.args[X_INDEX]
    raw_x = int(engine.gameState.resolve_variable(name))
    raw_y = int(engine.gameState.resolve_variable(instruction.args[Y_INDEX]))
    operator = instruction.args[OP_INDEX]
    try:
        x = int(raw_x)
        y = int(raw_y)
    except (ValueError, TypeError):
        raise BuildError(f"MATH: Cannot perform math on non-numeric values. "
                            f"x: '{raw_x}' ({type(raw_x).__name__}), "
                            f"y: '{raw_y}' ({type(raw_y).__name__})")
    if operator == "+":
        x += y
    elif operator == "-":
        x -= y
    elif operator == "*":
        x *= y
    elif operator == "/":
        if y == 0:
            raise BuildError("MATH: Division by zero.")
        x /= y
    elif operator == "%":
        if y == 0:
            raise BuildError("MATH: Modulo by zero.")
        x %= y
    else:
        raise BuildError("MATH: Invalid operator")

    engine.gameState.variables[name] = x
