from backend import BuildError

class Instruction:
    def __init__(self, name, args: list[str]):
        self.name = name
        self.args = args

    def run(self, engine):
        if self.name in engine.commandList:
            print(f"Running {self.name} {self.args}")
            return engine.commandList[self.name](self, engine)
        else:
            raise BuildError("Unrecognised command")
            return True