from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class BitShiftLeftWithOverflow(Instruction):
    name = "Bit Shift Left With Overflow"
    mnemonic = "BSLO"
    description = "Shifts the bits of variable 1 to the left by 1. The result is stored in variable 2. The remainder is stored in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "out", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() * 2))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSLO", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["RST", "zero"],
                ["BSROF", "PARAM1", "PARAM2", "zero", "PARAM3"]
            ]
        ]