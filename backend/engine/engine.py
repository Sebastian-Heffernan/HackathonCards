import os
import importlib
from backend.engine.commands import *
from backend.engine.classes.instruction import Instruction
from backend.compiler.rules import Rules
from backend.engine.classes.states import *
from backend.engine.classes.deck import *
from backend.BuildError import BuildError
import json
import re

class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")

class GameEngine:
    def __init__(self, rules : Rules):
        self.rules = rules
        self.decks = []
        self.stack = [] # for CALl pointer
        self.pointer = 0

        self.label = "SETUP"
        self.playerStates = []

        self.gameState = GameState()
        self.commandList = {}
        self._load_commands()

    def run_script(self, label="SETUP"):
        self.label = label
        self.pointer = 0

        while True:
            instruction = self.rules.labels[self.label][self.pointer]
            result = instruction.run(self)

            if result == "Break":
                break

            self.pointer += 1

    # Loads availabe commands into array
    def _load_commands(self):
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = f"backend.engine.commands.{filename[:-3]}" # remove extension
                module = importlib.import_module(module_name)
                # execute function in each file
                if hasattr(module, "execute"):
                    cmd_key = filename[:-3].upper()
                    self.commandList[cmd_key] = module.execute
    
    # Getters/setters
    def add_player(self, uuid):
        player = PlayerState(uuid)
        self.playerStates.append(player)
        self.gameState.playerCount += 1
    def get_current_player_uuid(self):
        return self.playerStates[self.gameState.turnPlayer].uuid
    def get_player_state(self, uuid):
        for player in self.playerStates:
            if player.uuid == uuid:
                return vars(player)
    def get_game_state(self):
        return vars(self.gameState)
    
    def get_deck(self, name):
        for deck in self.decks:
            if deck.name == name:
                return deck
        return None
    
    # gets the final object of a path like decks[0].name
    def resolve_path(self, obj, path):
        parts = path.split('.')
        for part in parts:
            match = re.match(r"(\w+)\[(\d+)\]", part) #array management
            if match:
                attr_name, index = match.groups()
                obj = getattr(obj, attr_name)
                obj = obj[int(index)]
            else:
                obj = getattr(obj, part)
        return obj



if __name__ == "__main__":
    rules2 = Rules()
    rules2.add_new_rule(0, "SETUP", [
        Instruction("DECK", ["MAKE", "deck"]),
        Instruction("DECK", ["SHUFFLE", "deck"]),
        Instruction("PRINT", ["decks[0].name"]),
        Instruction("CALL", ["TEST"]),
        Instruction("END_TURN", [0])
    ])
    rules2.add_new_rule(0, "TEST", [
        Instruction("RETURN", [0])
    ])
    engine = GameEngine(rules2)
    engine.run_script()
