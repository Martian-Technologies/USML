from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class BitwiseNor(Instruction):
    name = "Bitwise Nor"
    mnemonic = "BNOR"
    description = "Performs a bitwise NOR operation on the values of variable 1 and variable 2 and stores the result in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setArray([not(bits[0] or bits[1]) for bits in zip(memory[params[0]]["value"].getArray(), memory[params[1]]["value"].getArray())])

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BNOR", "PARAM1", "PARAM2", "PARAM3"]],
        ]