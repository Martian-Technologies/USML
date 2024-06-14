from instructions import instruction

class MultiplyLow(instruction.Instruction):
    name =  "Multiply Low"
    mnemonic = "MLL"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["MLL", "PARAM1", "PARAM2"]]]