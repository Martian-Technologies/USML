from param.param import Param
from instructions import instruction

class Copy(instruction.Instruction):
    name = "Copy"
    mnemonic = "CPY"
    
    def __init__(self):
        super().__init__()

    def setParam(self, paramNumber:int, param:Param):
        raise Exception(f"Failed adding param {param} at {paramNumber}. Defalt instruction has no params")

    def run(self):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return [
            [["CPY", "PARAM1", "PARAM2"]],
            [
                ["RST", "zero"],
                ["ADD", "PARAM1", "zero", "PARAM2"]
            ],
            [
                ["SET", "one", "1"],
                ["MLL", "PARAM1", "one", "PARAM2"]
            ]
        ]