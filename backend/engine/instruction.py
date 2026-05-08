
class Instruction:
    def __init__(self, name, args: list[str]):
        self.name = name
        self.args = args

    def run(self, engine):
        if self.name == "GOTO":
            print(f"going to {self.args[0]}")
            engine.pointer = 0
            engine.label = self.args[0]
        elif self.name in engine.commandList:
            engine.commandList[self.name](self, engine)