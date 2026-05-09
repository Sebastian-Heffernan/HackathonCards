class GameState:
    def __init__(self):
        self.turnPlayer = 0
        self.playerCount = 0
        self.variables = []

class PlayerState:
    def __init__(self):
        self.uuid = None
        self.variables = []
        self.hand = []