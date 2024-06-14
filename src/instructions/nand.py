from instructions import instruction

class Nand(instruction.Instruction):
    name =  "Nand"
    mnemonic = "NAND"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["NAND", "PARAM1", "PARAM2", "PARAM3"]]]