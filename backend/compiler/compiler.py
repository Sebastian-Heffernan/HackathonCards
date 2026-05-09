from backend.compiler.rules import Rules
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine


class CompilationError(Exception):
    """Exception raised for custom error scenarios.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Compiler:

    @staticmethod
    def skip_line(tokenized_line: str) -> bool:
        return (
            len(tokenized_line) == 0
            or tokenized_line[0] == ""
            or tokenized_line[0][0] == "#"
        )

    @staticmethod
    def compile(text_rules: str, command_list: dict):
        rules: Rules = Rules()

        text_rules.strip()
        tokenized_file = text_rules.split("\n")

        total_lines = len(tokenized_file)
        line_idx = 0

        while line_idx < total_lines:
            curr_line = tokenized_file[line_idx].strip()
            tokenized_line = curr_line.split(" ")

            if Compiler.skip_line(tokenized_line):
                line_idx += 1
                continue

            # Identify the rule (ACTION/LABEL)
            raw_new_label = tokenized_line[1]
            clean_new_label = raw_new_label.rstrip(":")
            line_idx += 1
            nodes = []

            # Process instructions until the next rule or end of file
            while line_idx < total_lines:
                curr_line = tokenized_file[line_idx].strip()
                tokenized_line = curr_line.split(" ")

                if Compiler.skip_line(tokenized_line):
                    line_idx += 1
                    continue

                if tokenized_line[0] not in command_list:
                    raise CompilationError(
                        f"Command ({tokenized_line[0]}) does not exist"
                    )

                # Check if this line is the start of a NEW rule
                if tokenized_line[0] == "LABEL":
                    break  # Stop inner loop, don't increment line_idx yet

                new_node = Instruction(tokenized_line[0], tokenized_line[1:])
                nodes.append(new_node)
                line_idx += 1

            # Save the rule before the outer loop starts the next one
            rules.add_new_rule(clean_new_label, nodes)

        return rules


if __name__ == "__main__":
    raw_text = """
    LABEL SETUP:
        GOTO TEST
    LABEL TEST:
        END_TURN
"""

    command_list: dict = GameEngine.load_commands()

    print(command_list)

    rules: Rules = Compiler.compile(raw_text, command_list)
    print(rules)
