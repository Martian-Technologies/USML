from pram.pram import Pram
from instructions import instruction

class Bool(instruction.Instruction):
    name = "Bool"
    mnemonic = "BOOL"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["BOOL", "PRAM1", "PRAM2"]],
            [
                ["RST", "zero"],
                ["NEQU", "PRAM1", "zero", "PRAM2"]
            ],
            [
                ["NOT", "PRAM1", "PRAM2"],
                ["NOT", "PRAM2", "PRAM2"]
            ]
        ]