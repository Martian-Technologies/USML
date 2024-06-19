from USML.instructions import instruction
from USML.bitString import BitString

class Swap(instruction.Instruction):
    name = "Swap"
    mnemonic = "SWP"
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