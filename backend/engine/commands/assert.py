from errors.BuildError import BuildError
from engine.classes.instruction import Instruction
from engine.classes.states import PlayerState
from engine.engine import GameEngine

LABEL = 0
PLAYER = 1

"""
ASSERT:
    makes a label into the player action
"""

# Player int is optional. If NULL then adds to ALL players
# ASSERT [label: str][player: int]
def execute(instruction: Instruction, engine: GameEngine):
    arg_count = len(instruction.args)
    
    if arg_count < 1:
        raise BuildError("ASSERT: [label] (Usage)")
    
    label = engine.gameState.resolve_variable(instruction.args[LABEL])
    if label not in engine.rules.labels:
        raise BuildError(f"ASSERT: Label '{label}' not found in rules.")
    
    # if no player then assert to all
    if arg_count == 1:
        for player in engine.playerStates:
            player.actions.append(label)
        return True
        
    player_idx = engine.gameState.resolve_variable(instruction.args[PLAYER])

    if not (0 <= player_idx < len(engine.playerStates)):
        raise BuildError(f"ASSERT: Player index {player_idx} out of range.")

    playerState: PlayerState = engine.playerStates[player_idx]
    playerState.actions.append(label)
