class GameState:
    def __init__(self):
        self.turnPlayer = 0
        self.playerCount = 0
        self.variables = {}

    #returns value of variable if found, else returns value
    def resolve_variable(self, value):
        #return if int, no processing
        if isinstance(value, int):
            return value
        # if value is actullay a variable name, return it's value
        if value in self.variables:
            return self.variables[value]
        #convert string to int
        try:
            return int(value)
        except ValueError:
            pass
        # hanlde literal values in "quotes"
        if isinstance(value, str):
            return value.strip('"')
    def get_variable(self, name):
        return self.variables.get(name, None)

class PlayerState:
    def __init__(self, uuid):
        self.uuid = uuid
        self.variables = []
        self.hand = []

    def resolve_variable(self, value):
        if value in self.variables:
            return self.variables[value]
        try:
            return int(value)
        except ValueError:
            return value