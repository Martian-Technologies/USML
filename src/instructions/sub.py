from instructions import instruction

class Sub(instruction.Instruction):
    name = "Sub"
    mnemonic = "SUB"
    
    def __init__(self):
        super().__init__()
