from instructions import instruction

class Bool(instruction.Instruction):
    name = "Bool"
    mnemonic = "BOOL"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["BOOL", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["NEQU", "PARAM1", "zero", "PARAM2"]
            ],
            [
                ["NOT", "PARAM1", "PARAM2"],
                ["NOT", "PARAM2", "PARAM2"]
            ]
        ]