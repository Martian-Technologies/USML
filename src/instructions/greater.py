from instructions import instruction

class Greater(instruction.Instruction):
    name =  "Greater"
    mnemonic = "GRT"
    
    def __init__(self):
        super().__init__()
