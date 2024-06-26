from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Print(Instruction):
    name = "Print"
    mnemonic = "PRINT"
    description = "Prints the value of variable 1 to the python console."
    expectedDataType = ["var"]
    usageTypes = ["in"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        print(memory[params[0]]["value"])

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [[["PRINT", "PARAM1"]]]