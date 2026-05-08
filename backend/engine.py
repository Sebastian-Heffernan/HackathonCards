import os
import importlib

class GameEngine:
    def init(self):
        self.commands = {}
        self._load_commands()
    def run_script(self, action_name):
        instructions = script
        pointer = 0
        while pointer < len(instructions):
            instruction = instructions[pointer]
            cmd = instruction["cmd"]
            args = instruction["args"]
            if cmd == "EXIT":
                break
            elif cmd == "GOTO":
                pointer = self._find_label(instructions, args[0])
                continue
            elif cmd in self.commands:
                self.commands[cmd](self, args)
            pointer += 1

    def _load_commands(self):
        path
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                module = importlib.import_module()
                self.commands[cmd]