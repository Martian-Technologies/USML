from instructions import instruction

class GreaterOrEqual(instruction.Instruction):
    name =  "Greater Or Equal"
    mnemonic = "GOE"
    
    def __init__(self):
        super().__init__()
