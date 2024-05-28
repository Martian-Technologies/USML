from param.param import Param
from instructions import instruction

class JumpIf(instruction.Instruction):
    name = "Jump If"
    mnemonic = "JMIF"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
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