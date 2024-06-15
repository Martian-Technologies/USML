from USML.instructions import instruction

class NotEquals(instruction.Instruction):
    name =  "Not Equals"
    mnemonic = "NEQU"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["NEQU", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["EQU", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]