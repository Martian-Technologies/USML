from instructions import instruction

class JumpIf(instruction.Instruction):
    name = "Jump If"
    mnemonic = "JMIF"
    
    def __init__(self):
        super().__init__()
