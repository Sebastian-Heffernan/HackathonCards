from backend.BuildError import BuildError
from backend.engine.classes.deck import Deck
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import PlayerState
from backend.engine.engine import GameEngine


# MOVE [Deck name][Player ID][Card ID]
# Get the player ID
# Move Card: 
# take card of players hand and move it to a deck. 
# Note: Remove Reveal Status
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError("MOVE requires 3 arguments")
    deck_name = instruction.args[0]
    player_id = engine.gameState.resolve_variable(instruction.args[1])
    card_id = engine.gameState.resolve_variable(instruction.args[2])

    ### get the deck to move card to
    target_deck: Deck = engine.get_deck(deck_name)
    if not target_deck:
        raise BuildError(f"Deck '{deck_name}' not found.")
    
    ### search for player via id
    if player_id < 0 or player_id >= len(engine.playerStates):
        raise BuildError()
    
    player = engine.playerStates[player_id]

    ### search for card via id
    if card_id < 0 or card_id >= len(player.hand):
        raise BuildError()
    
    card = player.hand.pop(card_id)
    engine.gameState.global_revealed[player_id].pop(card_id)
    target_deck.cards.append(card)
