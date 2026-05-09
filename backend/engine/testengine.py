from backend.engine.engine import GameEngine
from backend.compiler.compiler import Compiler
from backend.compiler.compiler import Rules


if __name__ == "__main__":
    test = """
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    DECK MAKE discard
    DECK CLEAR discard

    VARG SET i 0
    GOTO SETUPPLAYERS
# Will add 2 cards to each player
# Game setup
LABEL SETUPPLAYERS:
    VARG SET j 0
    CALL SETUPPLAYER
    # PRINT playerStates[i].hand
    ASSERT DRAW i
    ASSERT DISCARD i

    MATH i + 1
    COMPARE i < $playerCount
    GOTO SETUPPLAYERS
    END_TURN
LABEL SETUPPLAYER:
    DRAW deck i 1
    MATH j + 1
    COMPARE j < 2
    GOTO SETUPPLAYER
    RETURN
LABEL CONTINUE:
    # PRINT gameState.variables
    END_TURN $turnPlayer + 1
# Turn logic
LABEL DRAW:
    DRAW deck $turnPlayer 1
    GOTO CONTINUE

# Discarding logic
LABEL DISCARD:
    COMPARE -1 < $selectedCardId
    GOTO MOVE
    END_TURN
LABEL MOVE:
    VALUE TEMP $turnPlayer $selectedCardId
    # PRINT gameState.variables[TEMP]
    MOVE discard $turnPlayer $selectedCardId
    GOTO CONTINUE
"""
    black_jack = """
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    DECK MAKE discard
    DECK CLEAR discard
    ASSERT HIT
    ASSERT STAY
    # PRINT gameState.variables[$turnPlayer]
    VARG SET #e 0
    PRINT gameState.variables[#e]
    PRINT playerStates[#e]
    
LABEL HIT:
    DRAW deck $turnPlayer
    GOTO CALC

LABEL STAY:
    GOTO CALC

LABEL TEST:
    VARG SET a "hell"
    VARG SET b "hello"
    MATH b + 1
    COMPARE a == b
    END_TURN
    GOTO EXIT

LABEL EXIT:
    END_TURN
"""
    commandList = GameEngine.load_commands()
    rules: Rules = Compiler.compile(black_jack, commandList)
    engine = GameEngine(rules, commandList)
    # print(rules)
    engine.add_player(0)
    engine.add_player(1)
    engine.add_player(2)
    engine.run_script("TEST")
    # engine.gameState.variables["$selectedCardId"] = 1
    # engine.run_script("DISCARD")