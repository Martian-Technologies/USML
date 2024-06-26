from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Add(Instruction):
    name = "Add"
    mnemonic = "ADD"
    description = "Adds variables 1 and 2 together and stores it in variable 3."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(memory[params[0]]["value"].getInt() + memory[params[1]]["value"].getInt())

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["ADD", "PARAM1", "PARAM2", "PARAM3"]],
            [["ADDC", "PARAM1", "PARAM2", "PARAM3", "none"]],
        ]