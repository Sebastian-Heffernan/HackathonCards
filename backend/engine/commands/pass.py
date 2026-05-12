from errors.BuildError import BuildError
from engine.classes.deck import Deck
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.engine import GameEngine

def execute(instruction : Instruction, engine : GameEngine):
    return