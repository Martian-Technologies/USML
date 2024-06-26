from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Dereference(Instruction):
    name = "Dereference"
    mnemonic = "DREF"
    description = "Dereferences A ands stores the value in B"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = ["Need Memory Pos"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(memory[list(memory.keys())[memory[params[0]]["value"].getInt()]]["value"].getInt())

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["DREF", "PARAM1", "PARAM2"]],
        ]
    
    # do refeerence
    # list(memory.keys()).index(params[0])