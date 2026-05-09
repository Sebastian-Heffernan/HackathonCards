
class Instruction:
    def __init__(self, name, args: list[str]):
        self.name = name
        self.args = args

    def run(self, engine):
        if self.name in engine.commandList:
            engine.commandList[self.name](self, engine)
        else:
            print("Unrecognised command")