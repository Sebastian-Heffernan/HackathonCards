from backend.engine.classes.instruction import Instruction


class Rules:
    def __init__(self):
        self.labels = {}
        self.actions = {}

    def add_new_rule(
        self, is_action: bool, rule_name: str, instructions: list[Instruction]
    ):
        type_str = "ACTION" if is_action else "LABEL"
        print(
            f"[REGISTERED] {type_str}: {rule_name} ({len(instructions)} instructions)"
        )
        if is_action:
            self.actions[rule_name] = instructions
        else:
            self.labels[rule_name] = instructions

    def __str__(self):

        def format_section(title, data):
            if not data:
                return f"--- {title}: None ---"

            lines = [f"--- {title} ---"]
            for name, insts in data.items():
                # Joins instruction names with commas for a compact view
                inst_list = ", ".join(i.name for i in insts)
                lines.append(f"  ▶ {name}: [{inst_list}]")
            return "\n".join(lines)

        return "\n".join(
            [
                "\n" + "=" * 30,
                format_section("LABELS", self.labels),
                format_section("ACTIONS", self.actions),
                "=" * 30 + "\n",
            ]
        )
