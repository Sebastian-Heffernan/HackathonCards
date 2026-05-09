from backend.engine.classes.instruction import Instruction

def execute(instruction : Instruction, engine):
    print("Arguments:")
    for i in instruction.args:
        print(f"{i}")