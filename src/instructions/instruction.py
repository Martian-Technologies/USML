from __future__ import annotations
from param.param import Param

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    
    def __init__(self):
        self.params:list[Param] = []

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def getParam(self, paramNumber:int):
        if paramNumber >= 0 and len(self.params) > paramNumber:
            return self.params[paramNumber]
        return None

    def getParams(self):
        return self.params

    def run(self):
        raise Exception("Failed running instruction. Can not run defalt instruction")

    def getImplementations(self):
        raise Exception("Failed getting implementations. Defalt instruction has no implementations")

    def getMnemonic(self):
        return self.mnemonic

    def getName(self):
        return self.name