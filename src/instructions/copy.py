from instructions import instruction

class Copy(instruction.Instruction):
    name = "Copy"
    mnemonic = "CPY"
    
    def __init__(self):
        super().__init__()
