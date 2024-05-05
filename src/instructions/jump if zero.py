from instructions import instruction

class JumpIfZero(instruction.Instruction):
    name = "Jump If Zero"
    mnemonic = "JMZ"
    
    def __init__(self):
        super().__init__()
