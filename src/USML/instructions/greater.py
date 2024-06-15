from USML.instructions import instruction

class Greater(instruction.Instruction):
    name =  "Greater"
    mnemonic = "GRT"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["GRT", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["LOE", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]