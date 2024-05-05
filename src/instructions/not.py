from instructions import instruction

class Not(instruction.Instruction):
    name =  "Not"
    mnemonic = "NOT"
    
    def __init__(self):
        super().__init__()
