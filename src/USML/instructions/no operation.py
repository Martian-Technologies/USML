from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class NoOperation(Instruction):
    name =  "No Operation"
    mnemonic = "NOP"
    description = "Does nothing."
    expectedDataType = []
    usageTypes = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        pass

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["NOP"]],
            [
                ["JMP", "NoOperation"],
                [".NoOperation"]
            ]
        ]