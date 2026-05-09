### reveal
### specify which players card you are revealing, the card itself, and then also  and append it to global_revealed
### get the player who has their current turn from the game state, and then from there 
### everyones card is revealed at the same time
### 
### reveal lastmost (i - 1 card)
# REVEAL [PLAYER][card]

from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

