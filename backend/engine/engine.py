import importlib
import json
import os
import re

from errors.BuildError import BuildError
from compiler.rules import Rules
from engine.classes.deck import *
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.commands import *


class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")


class GameEngine:
    def __init__(self, rules: Rules, commandList: dict):
        self.debug = True
        self.rules = rules
        self.decks = []
        self.stack = []  # for CALL pointer
        self.pointer = 0

        # self.label = "SETUP"
        self.playerStates = []

        self.gameState = GameState()
        # self.commandList = {}
        self.commandList = commandList

    def run_script(self, label):
        self.label = label
        self.pointer = 0

        self.gameState.variables["$turnCount"] += 1
        print(f"[TURN {self.gameState.variables["$turnCount"]}]")
        # Perform instruction cycle
        while True:
            # Perform checks
            instruction = self.get_current_instruction()

            # print(instruction.name)
            result = instruction.run(self)

            if result == "break":
                break
            elif result == "jump":
                continue
            self.pointer += 1
        
    def get_current_instruction(self):
        if self.label not in self.rules.labels:
                raise BuildError(
                    f"Label '{self.label}' not found in script rules."
                )
        labelObj = self.rules.labels[self.label]
         # check pointer is in limit
        if not len(labelObj) > self.pointer:
            raise BuildError(
                f"Pointer at {self.pointer}, while label length was {len(labelObj)}"
                )
        return labelObj[self.pointer]

    # Loads availabe commands into array
    @staticmethod
    def load_commands() -> dict:
        commandList = {}
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = (
                    f"engine.commands.{filename[:-3]}"  # remove extension
                )
                module = importlib.import_module(module_name)
                # execute function in each file
                if hasattr(module, "execute"):
                    cmd_key = filename[:-3].upper()
                    commandList[cmd_key] = module.execute

        commandList["LABEL"] = ""
        return commandList

    ############################# Getters/setters #############################
    def add_player(self, uuid):
        player = PlayerState(uuid)
        self.playerStates.append(player)
        self.gameState.global_revealed.append([])  # new player means no hand
        self.gameState.variables["$playerCount"] += 1

    def get_current_player_uuid(self):
        return self.playerStates[self.gameState.variables["$turnPlayer"]].uuid

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
            match = re.match(r"(\w+)\[([^\]]+)\]", part)  # array management
            if match:
                attr_name, index_str = match.groups()
                if hasattr(obj, attr_name):
                    obj = getattr(obj, attr_name)
                elif isinstance(obj, dict) and attr_name in obj:
                    obj = obj[attr_name]
                else:
                    raise BuildError(f"Path Error: {obj} has no attribute/key '{attr_name}'")
                try:
                    idx = int(index_str)
                    obj = obj[int(idx)]
                except (ValueError, TypeError):
                    obj = obj[index_str] #treat as key for dictionary
                except KeyError:
                    obj = obj[str(index_str)]
                except IndexError:
                    raise BuildError(f"Index {index_str} out of bounds")
            else:
                obj = getattr(obj, part)
        return obj
