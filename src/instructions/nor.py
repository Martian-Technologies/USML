from instructions import instruction

class Nor(instruction.Instruction):

    name =  "Nor"
    mnemonic = "NOR"
    
    def __init__(self):
        super().__init__()
