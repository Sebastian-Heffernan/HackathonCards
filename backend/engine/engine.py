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
from backend.compiler.compiler import Compiler

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

    def run_script(self, label):
        self.label = label
        self.pointer = 0

        while True:
            instruction = self.rules.labels[self.label][self.pointer]
            # print(instruction.name)
            result = instruction.run(self)

            if result == "break":
                break
            elif result == "jump":
                continue
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
    raw_text = """
# SETUP
ACTION START:
    SHUFFLE deck
    MOVE_CARD deck active_zone
    SET_VAR score 0
    SET_VAR status "Game start"
LABEL SWAP_CARD:
    MOVE_CARD active_zone discard
    MOVE_CARD deck active_zone
    RETURN
ACTION GUESS_HIGHER:
    CALL SWAP_CARD
    GET_ATTR last_moved_card value next_val
    IF next_val > current_val GOTO WIN
    GOTO LOSE
ACTION GUESS_LOWER:
    CALL SWAP_CARD
    GET_ATTR last_moved_card value next_val
    IF next_val < current_val GOTO WIN
    GOTO LOSE
LABEL WIN:
    MATH score + 1
    SET_VAR current_val next_val
    SET_VAR status "Correct"
    EXIT
LABEL LOSE:
    SET_VAR status "Wrong"
    SET_VAR score 0
    GOTO START
"""
    test = """
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    CALL FUNC
    GOTO TEST
LABEL TEST:
    END_TURN
LABEL FUNC:
    PRINT decks[0].name
    RETURN
"""
    rules: Rules = Compiler.compile(test)
    engine = GameEngine(rules)
    engine.run_script("SETUP")
    # print(rules)
