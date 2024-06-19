from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftLeftWithOverflow(instruction.Instruction):
    name = "Bit Shift Left With Overflow"
    mnemonic = "BSLO"
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["BSLO", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["RST", "zero"],
                ["BSROF", "PARAM1", "PARAM2", "PARAM3", "zero"]
            ]
        ]