from USML.instructions import instruction
from USML.bitString import BitString

class Halt(instruction.Instruction):
    name = "Halt"
    mnemonic = "HLT"
    description = "Halts the program."
    expectedDataType = []
    usageTypes = []

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