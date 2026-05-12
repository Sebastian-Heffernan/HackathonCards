from compiler.compiler import Compiler
from compiler.rules import Rules
from backend.engine.classesOld.instruction import Instruction
from engine.engine import GameEngine

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


lobby_codes = {}
games = {}
rules_store = {}
