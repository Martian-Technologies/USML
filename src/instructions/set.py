from pram.pram import Pram
from instructions import instruction

class Set(instruction.Instruction):
    name = "Set"
    mnemonic = "SET"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [[["SET", "PRAM1", "PRAM2"]]]