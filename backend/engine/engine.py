import os
import importlib
from commands import *
import inspect

class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")

class GameEngine:
    def __init__(self, game_data):
        self.rules = game_data
        self.state = {

        }
        self.pointer = 0
        self.commandList = {}
        self._load_commands()

    def run_script(self, action_name):
        instructions = self.rules["scripts"]
        self.pointer = 0
        while self.pointer < len(instructions):
            instruction = instructions[self.pointer]
            cmd = instruction.command_name
            args = instruction.args
            if cmd == "EXIT":
                break
            elif cmd == "GOTO":
                self.pointer = self._find_label(instructions, instruction.args[0])
                continue
            elif cmd in self.commands:
                self.commands[cmd](self, args)
            self.pointer += 1

    def _load_commands(self):
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = f"command.{filename[:-3]}" # remove extension
                module = importlib.import_module(module_name)
                # execute for each in file
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        cmd_key = filename[:-3].upper()
                        self.commandList[cmd_key] = module.execute

    def _find_label(self, label_name):
        instructions = self.rules["scripts"]
        for i, instruction in enumerate(instructions):
            if instruction.command_name == "LABEL" and instruction.args[0] == label_name:
                return i
        return len(instructions)
    
if __name__ == "__main__":
    game_data = {
        "scripts": {
            
        }
    }
    engine = GameEngine()