from USML.instructions import instruction

class LessOrEqual(instruction.Instruction):
    name =  "Less Or Equal"
    mnemonic = "LOE"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["LOE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["GRT", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ],
            [
                ["LES", "PARAM1", "PARAM2", "PARAM3"],
                ["EQU", "PARAM1", "PARAM2", "isEqu"],
                ["OR", "PARAM3", "isEqu", "PARAM3"]
            ]
        ]