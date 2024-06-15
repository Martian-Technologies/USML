from USML.instructions import instruction

class Xor(instruction.Instruction):
    name =  "Xor"
    mnemonic = "XOR"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["XOR", "PARAM1", "PARAM2", "PARAM3"]]]