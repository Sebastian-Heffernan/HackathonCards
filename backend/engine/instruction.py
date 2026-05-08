class Instruction:
    def __init__(self, name, args: list[str]):
        self.name = name
        self.args = args

    def run(self, engine):
        self.args[0]
        print("test")