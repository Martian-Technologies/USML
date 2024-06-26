from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Sub(Instruction):
    name = "Sub"
    mnemonic = "SUB"
    description = "Subtracts the value of variable 2 from the value of variable 1 and stores the result in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(memory[params[0]]["value"].getInt() - memory[params[1]]["value"].getInt())

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [[["SUB", "PARAM1", "PARAM2", "PARAM3"]]]