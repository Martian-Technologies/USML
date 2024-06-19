from USML.instructions import instruction
from USML.bitString import BitString

class Reset(instruction.Instruction):
    name = "Reset"
    mnemonic = "RST"
    description = "Resets variable 1 to 0."
    expectedDataType = ["var"]
    usageTypes = ["out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(0)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["RST", "PARAM1"]],
            [
                ["SET", "PARAM1", "0"]
            ]
        ]