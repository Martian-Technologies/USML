from instructions import instruction

class JumpIfNot(instruction.Instruction):
    name = "Jump If Not"
    mnemonic = "JMNIF"
    
    def __init__(self):
        super().__init__()
