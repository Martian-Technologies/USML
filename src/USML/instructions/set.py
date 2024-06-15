from USML.instructions import instruction

class Set(instruction.Instruction):
    name = "Set"
    mnemonic = "SET"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["SET", "PARAM1", "PARAM2"]]
        ]