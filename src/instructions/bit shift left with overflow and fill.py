from instructions import instruction

class BitShiftLeftWithOverflowAndFill(instruction.Instruction):
    name = "Bit Shift Left With Overflow And Fill"
    mnemonic = "BSLOF"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSLOF", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]
        ]