from instructions import instruction

class Set(instruction.Instruction):
    name = "Set"
    mnemonic = "SET"
    
    def __init__(self):
        super().__init__()
