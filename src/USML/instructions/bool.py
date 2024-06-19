from USML.instructions import instruction
from USML.bitString import BitString

class Bool(instruction.Instruction):
    name = "Bool"
    mnemonic = "BOOL"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"].setInt(int(memory[params[0]]["value"].getInt() == 0))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["BOOL", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["NEQU", "PARAM1", "zero", "PARAM2"]
            ],
            [
                ["NOT", "PARAM1", "PARAM2"],
                ["NOT", "PARAM2", "PARAM2"]
            ]
        ]