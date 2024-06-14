from instructions import instruction

class JumpIf(instruction.Instruction):
    name = "Jump If"
    mnemonic = "JMIF"
    
    def __init__(self):
        super().__init__()

    def run(self, prams):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["JMIF", "PARAM1", "PARAM2"]],
            [
                ["JMIFN", "DontDoJump", "PARAM2"],
                ["JMP", "PARAM1"],
                [".DontDoJump"]
            ]
        ]