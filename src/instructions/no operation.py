from pram.pram import Pram
from instructions import instruction

class NoOperation(instruction.Instruction):
    name =  "No Operation"
    mnemonic = "NOP"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["NOP"]],
            [
                ["JMP", "NoOperation"],
                [".NoOperation"]
            ]
        ]