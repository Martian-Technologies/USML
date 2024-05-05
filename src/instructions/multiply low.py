from instructions import instruction

class MultiplyLow(instruction.Instruction):
    name =  "Multiply Low"
    mnemonic = "MLL"
    
    def __init__(self):
        super().__init__()
