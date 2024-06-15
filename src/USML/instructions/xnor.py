from USML.instructions import instruction

class Xnor(instruction.Instruction):
    name =  "Xnor"
    mnemonic = "XNOR"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["XNOR", "PARAM1", "PARAM2", "PARAM3"]]]