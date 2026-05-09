class GameState:
    def __init__(self):
        self.turnPlayer = 0
        self.playerCount = 0
        self.variables = []

    def resolve_variable(self, value):
        if value in self.variables:
            return self.variables[value]
        try:
            return int(value)
        except ValueError:
            return value

class PlayerState:
    def __init__(self):
        self.uuid = None
        self.variables = []
        self.hand = []

    def resolve_variable(self, value):
        if value in self.variables:
            return self.variables[value]
        try:
            return int(value)
        except ValueError:
            return value