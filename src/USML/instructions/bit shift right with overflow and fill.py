from USML.instructions import instruction
from USML.bitString import BitString

class BitShiftRightWithOverflowAndFill(instruction.Instruction):
    name = "Bit Shift Right With Overflow And Fill"
    mnemonic = "BSROF"
    expectedParams = ['var', 'var', 'var', 'var']
    
    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["BSROF", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]
        ]