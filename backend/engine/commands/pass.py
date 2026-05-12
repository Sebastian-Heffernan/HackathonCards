from errors.BuildError import BuildError
from backend.engine.classesOld.deck import Deck
from backend.engine.classesOld.instruction import Instruction
from backend.engine.classesOld.states import *
from engine.engine import GameEngine

def execute(instruction : Instruction, engine : GameEngine):
    return