from pram.pram import Pram
from instructions import instruction

class And(instruction.Instruction):
    name = "And"
    mnemonic = "AND"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["AND", "PRAM1", "PRAM2", "PRAM3"]],
            [
                ["NAND", "PRAM1", "PRAM2", "PRAM3"],
                ["NOT", "PRAM3", "PRAM3"]
            ]
        ]