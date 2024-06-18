from USML.instructions import instruction
from USML.bitString import BitString

class Not(instruction.Instruction):
    name =  "Not"
    mnemonic = "NOT"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(int(memory[params[0]]["value"].getInt() == 0))

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["NOT", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["EQU", "PARAM1", "zero", "PARAM2"]
            ],
            # [ what ?????
            #     ["BOOL", "PARAM1", "PARAM2"],
            #     ["NOT", "PARAM2", "PARAM2"]
            # ]
        ]