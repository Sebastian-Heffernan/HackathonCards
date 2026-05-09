### reveal
### specify which players card you are revealing, the card itself, and then also  and append it to global_revealed
### get the player who has their current turn from the game state, and then from there 
### everyones card is revealed at the same time
### 
### reveal lastmost (i - 1 card)
# REVEAL [PLAYER][card]

from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine
from backend.engine.classes.states import *

# REVEAL [PLAYER]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
        raise BuildError() 
    
    ## 
