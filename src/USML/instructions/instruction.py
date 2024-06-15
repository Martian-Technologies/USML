from __future__ import annotations
from USML.bitString import BitString

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    expectedParams = [] # list of 'var', 'num', 'label'
    
    def __init__(self):
        pass

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception("Failed running instruction. Can not run defalt instruction")

    def getImplementations(self) -> list[list[list[str]]]:
        raise Exception("Failed getting implementations. Defalt instruction has no implementations")

    def getMnemonic(self) -> str:
        return self.mnemonic

    def getName(self) -> str:
        return self.name
    
    def getExpectedParams(self) -> list[str]:
        return self.expectedParams