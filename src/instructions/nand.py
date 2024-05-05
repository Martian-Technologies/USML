from instructions import instruction

class Nand(instruction.Instruction):
    name =  "Nand"
    mnemonic = "NAND"
    
    def __init__(self):
        super().__init__()
