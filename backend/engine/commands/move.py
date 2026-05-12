from errors.BuildError import BuildError
from backend.engine.classesOld.deck import Deck
from backend.engine.classesOld.instruction import Instruction
from backend.engine.classesOld.states import *
from engine.engine import GameEngine


# MOVE [Deck name][Player ID][Card ID]
# Get the player ID
# Move Card: 
# take card of players hand and move it to a deck. 
# Note: Remove Reveal Status
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError("MOVE [DECK NAME][PLAYER ID][CARD ID]")
    deck_name = instruction.args[0]
    try:
        player_id = engine.gameState.resolve_variable(instruction.args[1])
        card_id = engine.gameState.resolve_variable(instruction.args[2])
    except (ValueError, TypeError):
        raise BuildError(f"MOVE: Player ID and Card ID must be integers. "
                         f"Got: {instruction.args[1]}, {instruction.args[2]}")

    ### get the deck to move card to
    target_deck: Deck = engine.get_deck(deck_name)
    if not target_deck:
        raise BuildError(f"MOVE: Deck '{deck_name}' not found.")
    
    ### search for player via id
    if not (0 <= player_id < len(engine.playerStates)):
        raise BuildError(f"MOVE: Player Index {player_id} out of bounds.")
    
    player = engine.playerStates[player_id]

    ### search for card via id
    if not (0 <= card_id < len(player.hand)):
        raise BuildError(f"MOVE: Card Index {card_id} out of bounds for Player {player_id}'s hand.")
    
    card = player.hand.pop(card_id)
    
    if player_id < len(engine.gameState.global_revealed):
        if card_id < len(engine.gameState.global_revealed[player_id]):
            engine.gameState.global_revealed[player_id].pop(card_id)

    target_deck.cards.append(card)
