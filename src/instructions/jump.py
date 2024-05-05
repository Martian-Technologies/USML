from instructions import instruction

class Jump(instruction.Instruction):
    name = "Jump"
    mnemonic = "JMP"
    
    def __init__(self):
        super().__init__()
