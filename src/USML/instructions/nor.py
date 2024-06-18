from USML.instructions import instruction
from USML.bitString import BitString

class Nor(instruction.Instruction):
    name =  "Nor"
    mnemonic = "NOR"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int((memory[params[0]]["value"].getInt() == 0) and (memory[params[1]]["value"].getInt() == 0)))

    def getImplementations(self) -> list[list[list[str]]]:
        return [[["NOR", "PARAM1", "PARAM2", "PARAM3"]]]