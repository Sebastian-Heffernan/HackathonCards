from backend.engine.engine import BaseCommand

class SetVar(BaseCommand):
    def execute(self, engine, args):
        var_name = args[0]
        value = args[1]

        if value.isDigit():
            value = int(value)
        engine.