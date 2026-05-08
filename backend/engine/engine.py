import os
import importlib
from commands import *
import inspect
from instruction import Instruction, InstructionEnd

class BaseCommand:
    def execute(self, engine, args):
        raise NotImplementedError("No execute")

class GameEngine:
    def __init__(self, game_data):
        self.rules = game_data
        self.state = {

        }
        self.commandList = {}
        self._load_commands()

    def run_script(self):
        pointer = 0
        label = "START"
        while 1:
            instruction : Instruction = self.rules["labels"][label][pointer]
            if instruction.name == "EXIT":
                print("exiting")
                break
            elif instruction.name == "GOTO":
                print(f"going to {instruction.args}")
                pointer = get_label_index(instruction)
                instruction = self.rules["labels"][instruction.args]
                continue
            elif instruction.name in self.commandList:
                self.commandList[instruction.name](self, instruction)
            instruction = instruction.next

    def _load_commands(self):
        path = os.path.join(os.path.dirname(__file__), "commands")
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module_name = f"commands.{filename[:-3]}" # remove extension
                print(f"loaded {module_name}")
                module = importlib.import_module(module_name)
                # execute for each in file
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        cmd_key = filename[:-3].upper()
                        self.commandList[cmd_key] = module.execute(self, None)

    def _find_label(self, label_name):
        instructions = self.rules["scripts"]
        for i, instruction in enumerate(instructions):
            if instruction.command_name == "LABEL" and instruction.args[0] == label_name:
                return i
        return len(instructions)
    
if __name__ == "__main__":
    game_data = {
        "labels": {
            "START": [
                Instruction("GOTO", ["TEST"]),
            ],
            "TEST": [
                Instrution("PRINT", ["test"])
                Instruction("EXIT", None)
            ]
        }
    }
    engine = GameEngine(game_data)
    engine.run_script()
