from USML.instructions import instruction
from USML.bitString import BitString

class Label(instruction.Instruction):
    name = "Label"
    mnemonic = "."
    expectedDataType = ["label"]
    usageTypes = ["out"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self) -> list[list[list[str]]]:
        return [[[".", "PARAM1"]]]