from pram.pram import Pram
from instructions import instruction

class Reset(instruction.Instruction):
    name = "Reset"
    mnemonic = "RST"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["RST", "PRAM1"]],
            [
                ["SET", "PRAM1", "0"]
            ]
        ]