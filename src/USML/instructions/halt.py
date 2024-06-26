from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Halt(Instruction):
    name = "Halt"
    mnemonic = "HLT"
    description = "Halts the program."
    expectedDataType = []
    usageTypes = []
    tags = ["program stop"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        return "END"

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["HLT"]],
            [
                [".Halt"],
                ["JMP", "Halt"]
            ]
        ]