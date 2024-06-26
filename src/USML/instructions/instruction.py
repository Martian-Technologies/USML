from __future__ import annotations
from USML.bitString import BitString

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    description = "Defalt instruction. Should not be used."
    expectedDataType = [] # list of "var", "num", "label"
    usageTypes = [] # list of "in", "out", "both"
    tags = [] # list of tags. Currently (Force Jump, Maybe Jump)

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception("Failed running instruction. Can not run defalt instruction")

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        raise Exception("Failed getting implementations. Defalt instruction has no implementations")
    
    @staticmethod
    def dealWithNumberData(numberData:str|int|float, memory:dict[str, dict[str, BitString|str|int]]):
        if type(numberData) == str:
            if numberData[0:1] == "&":
                return list(memory.keys()).index(numberData[1:len(numberData)])
            numberData = float(numberData)
        return numberData
    