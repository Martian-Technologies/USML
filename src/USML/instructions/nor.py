from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Nor(Instruction):
    name =  "Nor"
    mnemonic = "NOR"
    description = "Sets variable 3 to 1 if both variable 1 and variable 2 are 0, otherwise sets variable 3 to 0."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int((memory[params[0]]["value"].getInt() == 0) and (memory[params[1]]["value"].getInt() == 0)))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [[["NOR", "PARAM1", "PARAM2", "PARAM3"]]]