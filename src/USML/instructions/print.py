from USML.instructions import instruction
from USML.bitString import BitString

class Print(instruction.Instruction):
    name = "Print"
    mnemonic = "PRINT"
    expectedDataType = ["var"]
    usageTypes = ["in"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        print(memory[params[0]]["value"])

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [[["PRINT", "PARAM1"]]]