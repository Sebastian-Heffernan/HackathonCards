from backend.engine.TESTING.errors.BuildError import BuildError
from backend.engine.TESTING.classesOld.deck import Deck
from backend.engine.TESTING.classesOld.instruction import Instruction
from backend.engine.TESTING.classesOld.states import *
from backend.engine.TESTING.engine import GameEngine

def execute(instruction : Instruction, engine : GameEngine):
    return