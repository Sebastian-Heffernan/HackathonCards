from backend.engine.classes.instruction import Instruction
from backend import BuildError

# VARP [SET/MAKE][name][value]
def execute(instruction : Instruction, engine):
    if len(instruction.args) < 3:
        raise BuildError
    command = instruction.args[0]
    name = instruction.args[1]
    value = instruction.args[2]
    #if command == "SET":
