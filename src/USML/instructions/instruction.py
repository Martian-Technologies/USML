from __future__ import annotations

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    
    def __init__(self):
        pass

    def run(self, params):
        raise Exception("Failed running instruction. Can not run defalt instruction")

    def getImplementations(self):
        raise Exception("Failed getting implementations. Defalt instruction has no implementations")

    def getMnemonic(self):
        return self.mnemonic

    def getName(self):
        return self.name