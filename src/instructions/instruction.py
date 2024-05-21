from __future__ import annotations
from pram.pram import Pram

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    
    def __init__(self):
        self.prams:list[Pram] = []

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def getPram(self, pramNumber:int):
        if pramNumber >= 0 and len(self.prams) > pramNumber:
            return self.prams[pramNumber]
        return None

    def getPrams(self):
        return self.prams

    def run(self):
        raise Exception("Failed running instruction. Can not run defalt instruction")

    def getImplementations(self):
        raise Exception("Failed getting implementations. Defalt instruction has no implementations")

    def getMnemonic(self):
        return self.mnemonic

    def getName(self):
        return self.name