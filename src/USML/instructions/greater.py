from USML.instructions import instruction
from USML.bitString import BitString

class Greater(instruction.Instruction):
    name =  "Greater"
    mnemonic = "GRT"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int(memory[params[0]]["value"].getInt() > memory[params[1]]["value"].getInt()))

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["GRT", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["LOE", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]