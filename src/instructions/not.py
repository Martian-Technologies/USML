from instructions import instruction

class Not(instruction.Instruction):
    name =  "Not"
    mnemonic = "NOT"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["NOT", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["EQU", "PARAM1", "zero", "PARAM2"]
            ],
            [
                ["BOOL", "PARAM1", "PARAM2"],
                ["NOT", "PARAM2", "PARAM2"]
            ]
        ]