from instructions import instruction

class BitShiftLeftWithFill(instruction.Instruction):
    name = "Bit Shift Left With Fill"
    mnemonic = "BSLF"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSLF", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["BSROF", "PARAM1", "PARAM2", "none", "PARAM3"]
            ]
        ]