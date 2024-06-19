from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftRightWithFill(instruction.Instruction):
    name = "Bit Shift Right With Fill"
    mnemonic = "BSRF"
    description = "Shifts the bits of variable 1 to the right by 1 and fills the leftmost bit with the value of variable 3. The result is stored in variable 2."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "out", "in"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() / 2)
        memory[params[1]]["value"].setBit(memory[params[1]]["value"].bitCount-1, memory[params[2]]["value"].getInt() != 0)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSRF", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["BSROF", "PARAM1", "PARAM2", "PARAM3", "none"]
            ]
        ]