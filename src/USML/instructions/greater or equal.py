from USML.instructions import instruction

class GreaterOrEqual(instruction.Instruction):
    name =  "Greater Or Equal"
    mnemonic = "GOE"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["GOE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["LES", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ],
            [
                ["GRT", "PARAM1", "PARAM2", "PARAM3"],
                ["EQU", "PARAM1", "PARAM2", "isEqu"],
                ["OR", "PARAM3", "isEqu", "PARAM3"]
            ]
        ]