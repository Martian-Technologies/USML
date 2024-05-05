from instructions import instruction

class NotEquals(instruction.Instruction):
    name =  "Not Equals"
    mnemonic = "NEQU"
    
    def __init__(self):
        super().__init__()
