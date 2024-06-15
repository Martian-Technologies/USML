from USML.instructions import instruction

class IncrementIf(instruction.Instruction):
    name =  "Increment If"
    mnemonic = "INCI"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["INCI", "PARAM1", "PARAM2", "PARAM3"]]
            [
                ["JMIFN", "NoInc", "PARAM3"],
                ["INC", "PARAM1", "PARAM2"],
                [".NoInc"]
            ]
        ]