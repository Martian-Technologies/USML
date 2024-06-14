from instructions import instruction

class Increment(instruction.Instruction):
    name =  "Increment"
    mnemonic = "INC"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["INC", "PARAM1", "PARAM2"]],
            [
                ["SET", "one", "1"],
                ["INCI", "PARAM1", "PARAM2", "one"]
            ],
            [
                ["SET", "one", "1"],
                ["ADD", "PARAM1", "one", "PARAM2"]
            ]
        ]