from instructions import instruction

class Sub(instruction.Instruction):
    name = "Sub"
    mnemonic = "SUB"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["SUB", "PARAM1", "PARAM2", "PARAM3"]]]