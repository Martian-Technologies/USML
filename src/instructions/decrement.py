from param.param import Param
from instructions import instruction

class Decrement(instruction.Instruction):
    name =  "Decrement"
    mnemonic = "DEC"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["DEC", "PARAM1", "PARAM2"]],
            [
                ["SET", "one", "1"],
                ["DECI", "PARAM1", "PARAM2", "one"]
            ],
            [
                ["SET", "one", "1"],
                ["ADD", "PARAM1", "one", "PARAM2"]
            ]
        ]