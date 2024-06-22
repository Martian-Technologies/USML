from USML.instructions import instruction
from USML.bitString import BitString

class BitwiseAnd(instruction.Instruction):
    name = "Bitwise And"
    mnemonic = "BAND"
    description = "Performs a bitwise AND operation on the values of variable 1 and variable 2 and stores the result in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setArray([bits[0] and bits[1] for bits in zip(memory[params[0]]["value"].getArray(), memory[params[1]]["value"].getArray())])

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BAND", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["BNAND", "PARAM1", "PARAM2", "PARAM3"],
                ["BNOT", "PARAM3", "PARAM3"]
            ],
            [
                ["BNOT", "PARAM1", "not1"],
                ["BNOT", "PARAM1", "PARAM3"],
                ["BNOR", "PARAM3", "not1", "PARAM3"]
            ]
        ]