from USML.instructions import instruction
from USML.bitString import BitString

class MultiplyLow(instruction.Instruction):
    name =  "Multiply Low"
    mnemonic = "MLL"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(memory[params[0]]["value"].getInt() * memory[params[1]]["value"].getInt())

    def getImplementations(self) -> list[list[list[str]]]:
        return [[["MLL", "PARAM1", "PARAM2", "PARAM3"]]]