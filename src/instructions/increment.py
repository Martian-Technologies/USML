from pram.pram import Pram
from instructions import instruction

class Increment(instruction.Instruction):
    name =  "Increment"
    mnemonic = "INC"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["INC", "PRAM1", "PRAM2"]],
            [
                ["SET", "one", "1"],
                ["INCI", "PRAM1", "PRAM2", "one"]
            ],
            [
                ["SET", "one", "1"],
                ["ADD", "PRAM1", "one", "PRAM2"]
            ]
        ]