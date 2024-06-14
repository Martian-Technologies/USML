from instructions import instruction

class BitShiftRightWithOverflowAndFill(instruction.Instruction):
    name = "Bit Shift Right With Overflow And Fill"
    mnemonic = "BSROF"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSROF", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]
        ]