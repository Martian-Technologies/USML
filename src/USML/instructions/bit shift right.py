from USML.instructions import instruction

class BitShiftRight(instruction.Instruction):
    name = "Bit Shift Right"
    mnemonic = "BSR"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSR", "PARAM1", "PARAM2"]]
        ]