from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Swap(Instruction):
    name = "Swap"
    mnemonic = "SWP"
    description = "Swaps the values of variable 1 and variable 2."
    expectedDataType = ["var", "var"]
    usageTypes = ["both", "both"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        temp = memory[params[0]]["value"].copy()
        memory[params[0]]["value"] = memory[params[1]]["value"].copy()
        memory[params[1]]["value"] = temp

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["SWP", "PARAM1", "PARAM2"]],
            [
                ["CPY", "PARAM1", "TMP"],
                ["CPY", "PARAM2", "PARAM1"],
                ["CPY", "TMP", "PARAM2"]
            ],
        ]