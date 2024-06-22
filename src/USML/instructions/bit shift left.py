from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftLeft(instruction.Instruction):
    name = "Bit Shift Left"
    mnemonic = "BSL"
    description = "Shifts the bits of variable 1 to the left by 1. The result is stored in variable 2."
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    def __init__(self):
        super().__init__()

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() * 2)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSL", "PARAM1", "PARAM2"]],
            [["BSLO", "PARAM1", "PARAM2", "none"]],
        ]