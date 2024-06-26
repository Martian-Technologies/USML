from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Copy(Instruction):
    name = "Copy"
    mnemonic = "CPY"
    description = "Copies the value of variable 1 to variable 2."
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[1]]["value"] = memory[params[0]]["value"].copy()

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["CPY", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["ADD", "PARAM1", "zero", "PARAM2"]
            ],
            [
                ["SET", "one", "1"],
                ["MLL", "PARAM1", "one", "PARAM2"]
            ]
        ]