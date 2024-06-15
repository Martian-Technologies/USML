from USML.instructions import instruction

class Reset(instruction.Instruction):
    name = "Reset"
    mnemonic = "RST"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["RST", "PARAM1"]],
            [
                ["SET", "PARAM1", "0"]
            ]
        ]