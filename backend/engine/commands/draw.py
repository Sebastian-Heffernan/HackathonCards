from backend.BuildError import BuildError
from backend.engine.classes.deck import Deck
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import PlayerState
from backend.engine.engine import GameEngine

# DRAW [Deck Name][Player ID][Number]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) < 2:
        raise BuildError("DRAW requires 3 arguments")
    deck_name = instruction.args[0]
    player_i = engine.gameState.resolve_variable(instruction.args[1])
    count = engine.gameState.resolve_variable(instruction.args[2])
    target_deck : Deck = engine.get_deck(deck_name)
    # check that deck exits
    if not target_deck:
        raise BuildError(f"Deck '{deck_name}' not found.")
    # Safety check for player index
    if player_i >= len(engine.playerStates):
        raise BuildError(f"Player index {player_i} out of range.")
    target_player : PlayerState = engine.playerStates[player_i]

    #draw cards
    for i in range(count):
        #if deck has card
        if len(target_deck.cards) > 0:
            card = target_deck.cards.pop()
            target_player.hand.append(card)
        # TODO add when deck is empty check