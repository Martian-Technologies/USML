from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftLeft(instruction.Instruction):
    name = "Bit Shift Left"
    mnemonic = "BSL"
    expectedDataType = ["var", "var"]
    usageTypes = ["in", "out"]

    def __init__(self):
        super().__init__()
        
    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["BSL", "PARAM1", "PARAM2"]]
        ]