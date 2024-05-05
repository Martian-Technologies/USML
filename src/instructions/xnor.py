from instructions import instruction

class Xnor(instruction.Instruction):
    name =  "Xnor"
    mnemonic = "XNOR"
    
    def __init__(self):
        super().__init__()
