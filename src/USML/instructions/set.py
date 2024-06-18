from USML.instructions import instruction
from USML.bitString import BitString

class Set(instruction.Instruction):
    name = "Set"
    mnemonic = "SET"
    expectedDataType = ["var", "num"]
    usageTypes = ["out", None]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(params[1])

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["SET", "PARAM1", "PARAM2"]]
        ]