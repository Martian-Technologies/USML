from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class BitShiftLeftWithOverflowAndFill(Instruction):
    name = "Bit Shift Left With Overflow And Fill"
    mnemonic = "BSLOF"
    description = "Shifts the bits of variable 1 to the left by 1 and fills the rightmost bit with the value of variable 3. The result is stored in variable 2. The remainder is stored in variable 4."
    expectedDataType = ["var", "var", "var", "var"]
    usageTypes = ["in", "in", "out", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[3]]["value"].setInt(memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() * 2))
        memory[params[1]]["value"].setBit(0, memory[params[2]]["value"].getInt())

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSLOF", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]
        ]