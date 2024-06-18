from __future__ import annotations
from USML.bitString import BitString

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    expectedDataType = [] # list of "var", "num", "label"
    usageTypes = [] # list of "in", "out", "both"

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
    
    def getexpectedDataType(self) -> list[str]:
        return self.expectedDataType
    
    def getusageTypes(self) -> list[str]:
        return self.usageTypes