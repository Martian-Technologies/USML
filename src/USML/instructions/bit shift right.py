from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftRight(instruction.Instruction):
    name = "Bit Shift Right"
    mnemonic = "BSR"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[params[0]]["value"].getInt() / 2)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BSR", "PARAM1", "PARAM2"]]
        ]