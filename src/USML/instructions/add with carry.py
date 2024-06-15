from USML.instructions import instruction

class AddWithCarry(instruction.Instruction):
    name = "Add With Carry"
    mnemonic = "ADDC"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["ADDC", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]]