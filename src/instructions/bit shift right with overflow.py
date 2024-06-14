from instructions import instruction

class BitShiftRightWithOverflow(instruction.Instruction):
    name = "Bit Shift Right With Overflow"
    mnemonic = "BSRO"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSRO", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["RST", "zero"],
                ["BSROF", "PARAM1", "PARAM2", "PARAM3", "zero"]
            ]
        ]