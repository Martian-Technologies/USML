from param.param import Param
from instructions import instruction

class AddWithCarry(instruction.Instruction):
    name = "Add With Carry"
    mnemonic = "ADDC"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [[["ADDC", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]]