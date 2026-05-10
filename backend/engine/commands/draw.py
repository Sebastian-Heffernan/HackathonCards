from backend.errors.BuildError import BuildError
from backend.engine.classes.deck import Deck
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import PlayerState
from backend.engine.engine import GameEngine

"""
DRAW:
    Takes a card from deck name to a 
    players hand by number of times
"""

# DRAW [Deck Name][Player ID][Number]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 2:
        raise BuildError("DRAW [DECK NAME][PLAYER ID][NUMBER] (Usage)")
    deck_name = instruction.args[0]

    try:
        player_i = engine.gameState.resolve_variable(instruction.args[1])
        count = engine.gameState.resolve_variable(instruction.args[2])
    except (ValueError, TypeError):
        raise BuildError(f"DRAW Error: Player ID and Count must resolve to integers. "
                         f"Received: {instruction.args[1]}, {instruction.args[2]}")
    target_deck: Deck = engine.get_deck(deck_name)
    
    # check that deck exits
    if not target_deck:
        raise BuildError(f"Deck '{deck_name}' not found.")
    if not (0 <= player_i < len(engine.playerStates)):
        raise BuildError(f"DRAW Error: Player index {player_i} out of range.")
    # Safety check for player index
    if player_i >= len(engine.playerStates):
        raise BuildError(f"Player index {player_i} out of range.")
    target_player: PlayerState = engine.playerStates[player_i]

    # draw cards
    cards_drawn = 0
    for _ in range(count):
        # if deck has card
        if len(target_deck.cards) > 0:
            card = target_deck.cards.pop()
            target_player.hand.append(card)
            engine.gameState.global_revealed[player_i].append(False)
            cards_drawn += 1
        else:
            print(f"DEBUG: Deck '{deck_name}' ran out of cards.")
            break
    print(f"DEBUG: Player {player_i} drew {cards_drawn} cards from {deck_name}.")
