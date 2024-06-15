from USML.instructions import instruction

class Equals(instruction.Instruction):
    name = "Equals"
    mnemonic = "EQU"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["EQU", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NEQU", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]