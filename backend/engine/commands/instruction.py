class Instruction:
    def __init__(self, command_obj, name, args):
        self.command_obj = command_obj
        self.args = args
        self.name = name

    def run(self, engine):
        self.command.execute(engine, self.args)