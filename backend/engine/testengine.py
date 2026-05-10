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
    ASSERT HIGHER
    ASSERT LOWER
    VARG SET i 0
    CALL SETUP_PLAYERS

    DRAW deck 0 1
    REVEAL 0

    END_TURN

####### Deal cards
LABEL SETUP_PLAYERS:
    # VARG SET j 0
    # CALL DEAL_TO_PLAYER

    VARP SET i score 0
    VARP SET i isHigher 0

    MATH i + 1
    COMPARE i < $playerCount
    GOTO SETUP_PLAYERS
    RETURN
    
LABEL HIGHER:
    VARP SET $turnPlayer isHigher 1
    GOTO EXIT

LABEL LOWER:
    VARP SET $turnPlayer isHigher 0
    GOTO EXIT

LABEL EXIT:
    VARG SET temp $playerCount
    MATH temp - 1
    COMPARE $turnPlayer == temp
    CALL CALCULATE_START
    END_TURN $turnPlayer + 1

LABEL DRAW_CARD:
# Treat player 0 as dealer
    HANDLEN drawnInt 0
    DRAW deck 0 1
    REVEAL 0
    RETURN

LABEL CALCULATE_START:
    VARG SET i 0

    #if 5 cards end game
    HANDLEN totalCards 0
    COMPARE totalCards == 5
    GOTO FINISH_GAME
    
    CALL DRAW_CARD
    GOTO CALCULATE

LABEL CALCULATE:
    VALUE cardScore 0 drawnInt
    CALL CARD_TO_VALUE
    VARG SET drawnVal cardScore

    VARG SET prevInt drawnInt
    MATH prevInt - 1

    VALUE cardScore 0 prevInt
    CALL CARD_TO_VALUE
    VARG SET prevVal cardScore

    
    COMPARE drawnVal < prevVal
    GOTO LOWER_CALL_CALC
    GOTO HIGHER_CALL_CAL

# FInishe the loop after call
LABEL CALCULATE2:
    MATH i + 1
    COMPARE i < $playerCount
    GOTO CALCULATE
    RETURN

LABEL LOWER_CALL_CALC
    VARG PLAYER $turnPlayer isHigher
    VARG PLAYER $turnPlayer score
    COMPARE isHigher != 0
    MATH score + 1
    VARP SET $turnPlayer score score
    GOTO CALCULATE2

LABEL HIGHER_CALL_CAL:
    VARG PLAYER $turnPlayer isHigher
    VARG PLAYER $turnPlayer score
    COMPARE isHigher != 1
    MATH score + 1
    VARP SET $turnPlayer score score
    GOTO CALCULATE2

# 5 cards thus find who has highest score
LABEL FINISH_GAME:
    VARG SET highestScore 0
    VARG SET highestScoreInt 0
    VARG SET i 0
    CALL FINISH_GAME_LOOP
    VARG SET $winner highestScoreInt
    END_TURN

LABEL FINISH_GAME_LOOP:
    MATH i + 1
    COMPARE i == $playerCount
    RETURN

    # compare score with highest
    VARG PLAYER $turnPlayer score
    COMPARE score > highestScore
    GOTO FINISH_GAME_LOOP_HIGHER
    RETURN

LABEL FINISH_GAME_LOOP_HIGHER:
    VARG SET highestScore score
    VARG SET highestScoreInt $turnPlayer
    GOTO FINISH_GAME_LOOP

# Process card value
LABEL CARD_TO_VALUE:
    COMPARE cardValue == "A"
    GOTO CARD_A

    COMPARE cardValue == "K"
    GOTO CARD_K

    COMPARE cardValue == "Q"
    GOTO CARD_Q

    COMPARE cardValue == "J"
    GOTO CARD_J

    GOTO CARD_NUMBER

LABEL CARD_A:
    VARG SET cardScore 14
    RETURN

LABEL CARD_K:
    VARG SET cardScore 13
    RETURN

LABEL CARD_Q:
    VARG SET cardScore 12
    RETURN

LABEL CARD_J:
    VARG SET cardScore 11
    RETURN

LABEL CARD_NUMBER:
    VARG SET cardScore cardValue
    RETURN

# LABEL DEAL_TO_PLAYER:
#     DRAW deck i 1
#     MATH j + 1
#     COMPARE j < 2
#     GOTO DEAL_TO_PLAYER
#     RETURN
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

"""
give card to dealer
if higher
    true
    goto calc
if lower
    false
    goto calc
calc:
    if not last player
    end turn + 1
    draw card
    compare


"""