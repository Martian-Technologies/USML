from instructions import instruction

class Label(instruction.Instruction):
    name = "Label"
    mnemonic = "."
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[[".", "PARAM1"]]]