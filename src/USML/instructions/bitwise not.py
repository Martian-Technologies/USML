from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class BitwiseNot(Instruction):
    name = "Bitwise Not"
    mnemonic = "BNOT"
    description = "Performs a bitwise NOT operation on the values of variable 1 and stores the result in variable 2."
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setArray([not bit for bit in memory[params[0]]["value"].getArray()])

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BNOT", "PARAM1", "PARAM2"]],
            [["BNAND", "PARAM1", "PARAM1", "PARAM2"]],
            [["BNOR", "PARAM1","PARAM1", "PARAM2"]],
        ]