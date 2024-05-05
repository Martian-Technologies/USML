from instructions import instruction

class Reset(instruction.Instruction):
    name = "Reset"
    mnemonic = "RST"
    
    def __init__(self):
        super().__init__()
