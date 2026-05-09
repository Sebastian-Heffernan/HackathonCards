import os
import importlib
from backend.engine.commands import *
from backend.engine.instruction import Instruction
from backend.compiler.rules import Rules
from backend.engine.states import *
import json

class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")

class GameEngine:
    def __init__(self, rules : Rules):
        self.rules = rules
        self.pointer = 0
        
        self.label = "SETUP"
        self.playerStates = []

        self.gameState = GameState()
        self.commandList = {}
        self._load_commands()

    def run_script(self):
        while 1:
            instruction : Instruction = self.rules.labels[self.label][self.pointer]
            print(f"{self.pointer}: {instruction.name}")
            if instruction.name == "EXIT":
                print("exiting")
                break
            instruction.run(self)
            self.pointer += 1

    def _load_commands(self):
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = f"backend.engine.commands.{filename[:-3]}" # remove extension
                module = importlib.import_module(module_name)
                # execute function in each file
                if hasattr(module, "execute"):
                    cmd_key = filename[:-3].upper()
                    print(f"loaded {cmd_key}")
                    self.commandList[cmd_key] = module.execute

    def _find_label(self, label_name):
        instructions = self.rules["scripts"]
        for i, instruction in enumerate(instructions):
            if instruction.command_name == "LABEL" and instruction.args[0] == label_name:
                return i
        return len(instructions)
    
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

if __name__ == "__main__":
    rules = Rules()
    rules.add_new_rule(1, "SETUP", [
        Instruction("DECK", ["MAKE", "deck"]),
        Instruction("GOTO", ["START"])
    ])
    rules.add_new_rule(0, "START", [
        Instruction("DECK", ["SHUFFLE", "deck"]),
        Instruction("MOVE_CARD", ["deck", "active"]),
        Instruction("SET_VAR", ["score", "0"]),
        Instruction("SET_VAR", ["status", "\"Game start\""]),
        Instruction("END_TURN", None)
    ])
    rules.add_new_rule(0, "SWAP_CARD", [
        Instruction("MOVE_CARD", ["active", "discard"]),
        Instruction("MOVE_CARD", ["deck", "active"]),
        Instruction("RETURN", None)
    ])
    rules.add_new_rule(0, "HIGHER", [
        Instruction("CALL", ["SWAP_CARD"]),
        Instruction("GET_ATTR", ["last_moved_card", "value", "next_val"]),
        Instruction("COMPARE", ["next_val", ">", "current_val"]),
        Instruction("GOTO", ["WIN"]),
        Instruction("GOTO", ["LOSE"])
    ])
    rules.add_new_rule(0, "LOWER", [
        Instruction("CALL", ["SWAP_CARD"]),
        Instruction("GET_ATTR", ["last_moved_card", "value", "next_val"]),
        Instruction("COMPARE", ["next_val", "<", "current_val"]),
        Instruction("GOTO", ["WIN"]),
        Instruction("GOTO", ["LOSE"])
    ])
    rules.add_new_rule(0, "WIN", [
        Instruction("MATH", ["score", "+", "1"]),
        Instruction("SET_VAR", ["current_val", "next_val"]),
        Instruction("SET_VAR", ["status", "\"Correct\""]),
        Instruction("GOTO", ["START"])
    ])
    rules.add_new_rule(0, "LOSE", [
        Instruction("SET_VAR", ["score", "0"]),
        Instruction("SET_VAR", ["status", "\"Wrong\""]),
        Instruction("GOTO", ["START"])
    ])
    # engine = GameEngine(rules)
    # engine.run_script()
