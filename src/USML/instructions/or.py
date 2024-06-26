from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Or(Instruction):
    name =  "Or"
    mnemonic = "OR"
    description = "Sets variable 3 to 1 if either variable 1 or variable 2 are 1, otherwise sets variable 3 to 0."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int((memory[params[0]]["value"].getInt() != 0) or (memory[params[1]]["value"].getInt() != 0)))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["OR", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NOR", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]