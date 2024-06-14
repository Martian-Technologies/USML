from instructions import instruction

class Add(instruction.Instruction):
    name = "Add"
    mnemonic = "ADD"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["ADD", "PARAM1", "PARAM2", "PARAM3"]]]