from instructions import instruction

class Bool(instruction.Instruction):
    name = "Bool"
    mnemonic = "BOOL"
    
    def __init__(self):
        super().__init__()
