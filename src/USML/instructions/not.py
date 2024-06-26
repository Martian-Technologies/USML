from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Not(Instruction):
    name =  "Not"
    mnemonic = "NOT"
    description = "Sets variable 2 to 1 if variable 1 is 0, otherwise sets variable 2 to 0."
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(int(memory[params[0]]["value"].getInt() == 0))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
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