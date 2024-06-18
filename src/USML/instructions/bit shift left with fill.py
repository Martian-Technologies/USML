from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftLeftWithFill(instruction.Instruction):
    name = "Bit Shift Left With Fill"
    mnemonic = "BSLF"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["BSLF", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["BSROF", "PARAM1", "PARAM2", "none", "PARAM3"]
            ]
        ]