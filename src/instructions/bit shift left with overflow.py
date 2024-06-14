from instructions import instruction

class BitShiftLeftWithOverflow(instruction.Instruction):
    name = "Bit Shift Left With Overflow"
    mnemonic = "BSLO"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSLO", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["RST", "zero"],
                ["BSROF", "PARAM1", "PARAM2", "PARAM3", "zero"]
            ]
        ]