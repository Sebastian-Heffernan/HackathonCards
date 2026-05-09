import importlib
import json
import os
import re

from backend.BuildError import BuildError
from backend.compiler.rules import Rules
from backend.engine.classes.deck import *
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.commands import *


class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")


class GameEngine:
    def __init__(self, rules: Rules, commandList: dict):
        self.rules = rules
        self.decks = []
        self.stack = []  # for CALL pointer
        self.pointer = 0

        self.label = "SETUP"
        self.playerStates = []

        self.gameState = GameState()
        self.commandList = {}
        self.commandList = commandList

    def run_script(self, label):
        self.label = label
        self.pointer = 0

        self.gameState.variables["turnCount"] += 1
        while True:
            # check if label exits
            if self.label not in self.rules.labels:
                raise BuildError(
                    f"Runtime Error: Label '{self.label}' not found in script rules."
                )
            labelObj = self.rules.labels[self.label]
            # check pointer is in limit
            if not len(labelObj) > self.pointer:
                break
            instruction = labelObj[self.pointer]
            # print(instruction.name)
            result = instruction.run(self)

            if result == "break":
                break
            elif result == "jump":
                continue
            self.pointer += 1

    # Loads availabe commands into array
    @staticmethod
    def load_commands() -> dict:
        commandList = {}
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = (
                    f"backend.engine.commands.{filename[:-3]}"  # remove extension
                )
                module = importlib.import_module(module_name)
                # execute function in each file
                if hasattr(module, "execute"):
                    cmd_key = filename[:-3].upper()
                    commandList[cmd_key] = module.execute

        commandList["LABEL"] = ""
        return commandList

    # Getters/setters
    def add_player(self, uuid):
        player = PlayerState(uuid)
        self.playerStates.append(player)
        self.gameState.global_revealed.append([])  # new player means no hand
        self.gameState.variables["playerCount"] += 1

    def get_current_player_uuid(self):
        return self.playerStates[self.gameState.variables["turnPlayer"]].uuid

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
        parts = path.split(".")
        for part in parts:
            match = re.match(r"(\w+)\[(\d+)\]", part)  # array management
            if match:
                attr_name, index = match.groups()
                obj = getattr(obj, attr_name)
                obj = obj[int(index)]
            else:
                obj = getattr(obj, part)
        return obj


if __name__ == "__main__":
    test = """
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    DECK MAKE discard
    DECK CLEAR discard

    VARG SET i 0
    GOTO SETUPPLAYERS
# Will add 2 cards to each player
# Game setup
LABEL SETUPPLAYERS:
    VARG SET j 0
    CALL SETUPPLAYER
    PRINT playerStates[i].hand
    ASSERT DRAW i
    ASSERT DISCARD i

    MATH i + 1
    COMPARE i < playerCount
    GOTO SETUPPLAYERS
    END_TURN
LABEL SETUPPLAYER:
    DRAW deck i 1
    MATH j + 1
    COMPARE j < 2
    GOTO SETUPPLAYER
    RETURN
LABEL CONTINUE:
    # PRINT gameState.variables
    END_TURN turnPlayer + 1
# Turn logic
LABEL DRAW:
    DRAW deck turnPlayer 1
    GOTO CONTINUE
LABEL DISCARD:
    MOVE discard turnPlayer $selectedCardId
    GOTO CONTINUE
"""

    test2 = """
LABEL SETUP:
    GOTO ADDCARDSTOALL
LABEL ADDCARDSTOALL:
    END_TURN
"""
    rules: Rules = Compiler.compile(test)
    # print(rules)
    engine = GameEngine(rules)
    engine.add_player(0)
    engine.add_player(1)
    engine.add_player(2)
    engine.run_script("SETUP")
