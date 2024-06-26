from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Set(Instruction):
    name = "Set"
    mnemonic = "SET"
    description = "Sets variable 1 to the value of variable 2."
    expectedDataType = ["var", "num"]
    usageTypes = ["out", None]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(Instruction.dealWithNumberData(params[1], memory))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["SET", "PARAM1", "PARAM2"]]
        ]