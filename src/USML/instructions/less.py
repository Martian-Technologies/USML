from USML.instructions import instruction

class Less(instruction.Instruction):
    name =  "Less"
    mnemonic = "LES"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["LES", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["GOE", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]