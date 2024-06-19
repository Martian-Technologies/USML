from USML.instructions import instruction
from USML.bitString import BitString

class And(instruction.Instruction):
    name = "And"
    mnemonic = "AND"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(int((memory[params[0]]["value"].getInt() != 0) and (memory[params[0]]["value"].getInt() != 0)))

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["AND", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NAND", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]