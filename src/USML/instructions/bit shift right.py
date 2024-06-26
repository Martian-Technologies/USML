from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class BitShiftRight(Instruction):
    name = "Bit Shift Right"
    mnemonic = "BSR"
    description = "Shifts the bits of variable 1 to the right by 1. The result is stored in variable 2."
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() / 2)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSR", "PARAM1", "PARAM2"]],
            [["BSRO", "PARAM1", "PARAM2", "none"]],
        ]