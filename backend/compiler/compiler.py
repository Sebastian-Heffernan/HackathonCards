from backend.compiler.rules import Rules
from backend.engine.instruction import Instruction


class Compiler:

    @staticmethod
    def skip_line(tokenized_line: str) -> bool:
        return (
            len(tokenized_line) == 0
            or tokenized_line[0] == ""
            or tokenized_line[0][0] == "#"
        )

    @staticmethod
    def compile(text_rules: str):
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
            raw_new_rule = tokenized_line[1]
            clean_new_rule = raw_new_rule.rstrip(":")
            line_idx += 1
            nodes = []

            # Process instructions until the next rule or end of file
            while line_idx < total_lines:
                curr_line = tokenized_file[line_idx].strip()
                tokenized_line = curr_line.split(" ")

                if Compiler.skip_line(tokenized_line):
                    line_idx += 1
                    continue

                # Check if this line is the start of a NEW rule
                if tokenized_line[0] in ["ACTION", "LABEL"]:
                    break  # Stop inner loop, don't increment line_idx yet

                new_node = Instruction(tokenized_line[0], tokenized_line[1:])
                nodes.append(new_node)
                line_idx += 1

            # Save the rule before the outer loop starts the next one
            rules.add_new_rule(curr_line.startswith("ACTION"), clean_new_rule, nodes)

        return rules


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

    rules: Rules = Compiler.compile(raw_text)
    print(rules)
