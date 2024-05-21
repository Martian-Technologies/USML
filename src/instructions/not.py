from pram.pram import Pram
from instructions import instruction

class Not(instruction.Instruction):
    name =  "Not"
    mnemonic = "NOT"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["NOT", "PRAM1", "PRAM2"]],
            [
                ["RST", "zero"],
                ["EQU", "PRAM1", "zero", "PRAM2"]
            ],
            [
                ["BOOL", "PRAM1", "PRAM2"],
                ["NOT", "PRAM2", "PRAM2"]
            ]
        ]