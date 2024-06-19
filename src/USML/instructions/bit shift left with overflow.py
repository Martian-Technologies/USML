from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftLeftWithOverflow(instruction.Instruction):
    name = "Bit Shift Left With Overflow"
    mnemonic = "BSLO"
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