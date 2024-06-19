from USML.instructions import instruction
from USML.bitString import BitString

class LessOrEqual(instruction.Instruction):
    name =  "Less Or Equal"
    mnemonic = "LOE"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int(memory[params[0]]["value"].getInt() <= memory[params[1]]["value"].getInt()))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["LOE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["GRT", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ],
            [
                ["LES", "PARAM1", "PARAM2", "PARAM3"],
                ["EQU", "PARAM1", "PARAM2", "isEqu"],
                ["OR", "PARAM3", "isEqu", "PARAM3"]
            ]
        ]