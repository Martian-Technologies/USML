from instructions import instruction

class Halt(instruction.Instruction):
    name = "Halt"
    mnemonic = "HLT"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["HLT"]],
            [
                [".Halt"],
                ["JMP", "Halt"]
            ]
        ]