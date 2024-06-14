from instructions import instruction

class Nor(instruction.Instruction):

    name =  "Nor"
    mnemonic = "NOR"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["NOR", "PARAM1", "PARAM2", "PARAM3"]]]