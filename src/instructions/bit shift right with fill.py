from instructions import instruction

class BitShiftRightWithFill(instruction.Instruction):
    name = "Bit Shift Right With Fill"
    mnemonic = "BSRF"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSRF", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["BSROF", "PARAM1", "PARAM2", "none", "PARAM3"]
            ]
        ]