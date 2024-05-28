from param.param import Param
from instructions import instruction

class MultiplyLow(instruction.Instruction):
    name =  "Multiply Low"
    mnemonic = "MLL"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["MLL", "PARAM1", "PARAM2"]]]