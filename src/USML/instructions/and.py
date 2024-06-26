from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class And(Instruction):
    name = "And"
    mnemonic = "AND"
    description = "Sets variable 3 to 1 if variable 1 and variable 2 are both not 0, otherwise sets variable 3 to 0."
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
            ],
            [
                ["NOT", "PARAM1", "not1"],
                ["NOT", "PARAM1", "PARAM3"],
                ["NOR", "PARAM3", "not1", "PARAM3"]
            ]
        ]