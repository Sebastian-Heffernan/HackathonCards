from backend.engine.TESTING.errors import BuildError

class Instruction:
    def __init__(self, name, args: list[str]):
        self.name = name
        self.args = args
        self.index = None #for storing index in og Text file TODO

    def run(self, engine):
        if self.name in engine.commandList:
            if engine.debug:
                print(f"    [I] {self.name}: {self.args}")
            return engine.commandList[self.name](self, engine)
        else:
            raise BuildError("Unrecognised command")
        