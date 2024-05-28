from param.param import Param
from instructions import instruction

class Jump(instruction.Instruction):
    name = "Jump"
    mnemonic = "JMP"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["JMP", "PARAM1"]],
            [
                ["SET", "one", "1"],
                ["JMIF", "PARAM1", "one"]
            ],
            [
                ["RST", "zero"],
                ["JMIFN", "PARAM1", "zero"]
            ]
        ]