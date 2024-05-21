from pram.pram import Pram
from instructions import instruction

class Copy(instruction.Instruction):
    name = "Copy"
    mnemonic = "CPY"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["CPY", "PRAM1", "PRAM2"]],
            [
                ["RST", "zero"],
                ["ADD", "PRAM1", "zero", "PRAM2"]
            ],
            [
                ["SET", "one", "1"],
                ["MLL", "PRAM1", "one", "PRAM2"]
            ]
        ]