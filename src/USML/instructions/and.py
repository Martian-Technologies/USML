from USML.instructions import instruction
from USML.bitString import BitString

class And(instruction.Instruction):
    name = "And"
    mnemonic = "AND"
    description = "Performs a bitwise AND operation on variables 1 and 2 and stores the result in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(int((memory[params[0]]["value"].getInt() != 0) and (memory[params[0]]["value"].getInt() != 0)))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["AND", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NAND", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]