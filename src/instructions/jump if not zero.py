from instructions import instruction

class JumpIfNotZero(instruction.Instruction):
    name = "Jump If Not Zero"
    mnemonic = "JMNZ"
    
    def __init__(self):
        super().__init__()
