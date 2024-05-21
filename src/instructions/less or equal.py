from pram.pram import Pram
from instructions import instruction

class LessOrEqual(instruction.Instruction):
    name =  "Less Or Equal"
    mnemonic = "LOE"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["LOE", "PRAM1", "PRAM2", "PRAM3"]],
            [
                ["GRT", "PRAM1", "PRAM2", "PRAM3"],
                ["NOT", "PRAM3", "PRAM3"]
            ],
            [
                ["LES", "PRAM1", "PRAM2", "PRAM3"],
                ["EQU", "PRAM1", "PRAM2", "isEqu"],
                ["OR", "PRAM3", "isEqu", "PRAM3"]
            ]
        ]