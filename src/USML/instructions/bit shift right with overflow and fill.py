from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftRightWithOverflowAndFill(instruction.Instruction):
    name = "Bit Shift Right With Overflow And Fill"
    mnemonic = "BSROF"
    expectedDataType = ["var", "var", "var", "var"]
    usageTypes = ["in", "out", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() / 2)
        memory[params[3]]["value"].setInt(memory[params[0]]["value"].getInt() % 2)
        memory[params[1]]["value"].setBit(memory[params[1]]["value"].bitCount-1, memory[params[2]]["value"].getInt() != 0)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSROF", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]
        ]