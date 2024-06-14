from instructions import instruction

class BitShiftLeft(instruction.Instruction):
    name = "Bit Shift Left"
    mnemonic = "BSL"
    
    def __init__(self):
        super().__init__()
        
    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BSL", "PARAM1", "PARAM2"]]
        ]