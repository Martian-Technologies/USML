from USML.instructions import instruction

class JumpIfNot(instruction.Instruction):
    name = "Jump If Not"
    mnemonic = "JMIFN"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["JMIFN", "PARAM1", "PARAM2"]],
            [
                ["JMIF", "DontDoJump", "PARAM2"],
                ["JMP", "PARAM1"],
                [".DontDoJump"]
            ]
        ]