LABEL = 0
PLAYER = 1


# ASSERT [label: str][player: int]
def execute(instruction: Instruction, engine: GameEngine):
    label = instruction.arg[LABEL]
    player_idx = instruction.arg[PLAYER]

    playerState: PlayerState = engine.playerStates[player_idx]
