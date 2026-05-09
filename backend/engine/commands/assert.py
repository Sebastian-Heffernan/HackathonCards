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
        raise BuildError()

    label = instruction.args[LABEL]
    player_idx = int(instruction.args[PLAYER])

    if label not in engine.rules.labels:
        raise BuildError()

    playerState: PlayerState = engine.playerStates[player_idx]
    playerState.actions.append(label)
