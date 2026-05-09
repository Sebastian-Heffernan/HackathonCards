from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import PlayerState
from backend.engine.engine import GameEngine

LABEL = 0
PLAYER = 1

"""
ASSERT:
    makes a label into the player action
"""


# ASSERT [label: str][player: int]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 2:
        raise BuildError("ASSERT requires 2 arguments: [label] [player_index]")

    label = engine.gameState.resolve_variable(instruction.args[LABEL])
    player_idx = engine.gameState.resolve_variable(instruction.args[PLAYER])

    if label not in engine.rules.labels:
        raise BuildError(f"ASSERT Error: Label '{label}' not found in rules.")
    if not (0 <= player_idx < len(engine.playerStates)):
        raise BuildError(f"ASSERT Error: Player index {player_idx} out of range.")

    playerState: PlayerState = engine.playerStates[player_idx]
    playerState.actions.append(label)
