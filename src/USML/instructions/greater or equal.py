from USML.instructions import instruction
from USML.bitString import BitString

class GreaterOrEqual(instruction.Instruction):
    name =  "Greater Or Equal"
    mnemonic = "GOE"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int(memory[params[0]]["value"].getInt() >= memory[params[1]]["value"].getInt()))

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["GOE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["LES", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ],
            [
                ["GRT", "PARAM1", "PARAM2", "PARAM3"],
                ["EQU", "PARAM1", "PARAM2", "isEqu"],
                ["OR", "PARAM3", "isEqu", "PARAM3"]
            ]
        ]