from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class DereferenceWrite(Instruction):
    name = "DereferenceWrite"
    mnemonic = "DREFW"
    description = "Stores the value in B in memory position A points to"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "in"] # ?? idk what happens here
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[list(memory.keys())[memory[params[0]]["value"].getInt()]]["value"].setInt(memory[params[1]]["value"].getInt())

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["DREFW", "PARAM1", "PARAM2"]],
        ]
    
    # do refeerence
    # list(memory.keys()).index(params[0])