from USML.instructions import instruction
from USML.bitString import BitString

class NoOperation(instruction.Instruction):
    name =  "No Operation"
    mnemonic = "NOP"
    expectedDataType = []
    usageTypes = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        pass

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["NOP"]],
            [
                ["JMP", "NoOperation"],
                [".NoOperation"]
            ]
        ]