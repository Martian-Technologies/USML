from instructions import instruction

class And(instruction.Instruction):
    name = "And"
    mnemonic = "AND"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["AND", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NAND", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]