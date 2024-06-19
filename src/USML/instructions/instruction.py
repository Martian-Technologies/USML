from __future__ import annotations
from USML.bitString import BitString

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    expectedDataType = [] # list of "var", "num", "label"
    usageTypes = [] # list of "in", "out", "both"
    tags = [] # list of tags. Currently (Force Jump, Maybe Jump)

    def __init__(self):
        pass

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception("Failed running instruction. Can not run defalt instruction")