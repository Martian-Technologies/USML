from USML.instructions import instruction

class NoOperation(instruction.Instruction):
    name =  "No Operation"
    mnemonic = "NOP"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["NOP"]],
            [
                ["JMP", "NoOperation"],
                [".NoOperation"]
            ]
        ]