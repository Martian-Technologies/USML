from param.param import Param
from instructions import instruction

class Or(instruction.Instruction):
    name =  "Or"
    mnemonic = "OR"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["OR", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NOR", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]